from bs4 import BeautifulSoup
import requests
import sys
from pymongo import MongoClient

data = []


# connect to mongodb and get the collection
def mongo_connection():
    cluster = MongoClient("mongodb+srv://doriyaspielman:1234@cluster0-spfhl.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["firmware_data"]
    firmware_collection = db["firmware"]
    return firmware_collection

# get and insert the data
def get_data(source, date ,colection):
    soup = BeautifulSoup(source, 'lxml')  # parsing
    # go over every device
    for product in soup.find_all('tr', class_=['even', 'odd']):
        # extract and add device name
        name = product.a.text

        # extract version
        version = product.find('td', class_='views-field views-field-field-android-version2').text.strip()

        info = {
            'Device name': name,
            'Version': version,
            'Build date': date
        }
        # check if the document exists
        if colection.count_documents(info) == 0:
            data.append(info)

        # check if we are not at the last page
    if soup.find('li', class_='pager-next last').find('a'):
        global new_url
        # update url for next page
        new_url = soup.find('li', class_='pager-next last').find('a')['href']
    else:
        # if we got to the last pagee - stop while lop
        new_url = 0


def get_build_date(url):
    last_modified = ""
    header = requests.head(url).headers
    # get build date from page header
    if 'Last-Modified' in header:
        last_modified = header['Last-Modified']
    return last_modified


# save the url from input
baseUrl = sys.argv[1]
# go to downloads page for the data
src = requests.get(baseUrl + 'firmware-downloads').text
build_date = get_build_date(baseUrl + 'firmware-downloads')
col = mongo_connection()
get_data(src, build_date, col)


# go over all pages to get all the data
while new_url != 0:
    # request the new url
    src = requests.get(baseUrl + new_url).text
    build_date = get_build_date(baseUrl + new_url)
    get_data(src, build_date, col)
# if data is not empty - insert to database
if data:
    col.insert(data)

