from bs4 import BeautifulSoup
import requests
from datetime import date
import sys
import pymongo
from pymongo import MongoClient

data = []


# get mongodb collection
def mongo_connection():
    cluster = MongoClient("mongodb+srv://doriyaspielman:1234@cluster0-spfhl.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["firmware_data"]
    collection = db["firmware"]
    return collection

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


# save the url from input
baseUrl = sys.argv[1]
# go to downloads page for the data
src = requests.get(baseUrl + 'firmware-downloads').text
header = requests.head(baseUrl + 'firmware-downloads').headers
# get build date from page header
if 'Last-Modified' in header:
    last_modified = header['Last-Modified']
col = mongo_connection()
get_data(src, last_modified, col)


# go over all pages to get all the data
while new_url != 0:
    # request the new url
    src = requests.get(baseUrl + new_url).text
    header = requests.head(baseUrl + new_url).headers
    if 'Last-Modified' in header:
        last_modified = header['Last-Modified']
    get_data(src, last_modified, col)
# if data is not empty - insert to database
if data:
    col.insert(data)