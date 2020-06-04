from bs4 import BeautifulSoup
import requests
import sys
from pymongo import MongoClient



# connect to mongodb and get the collection
def mongo_connection():
    cluster = MongoClient("mongodb+srv://doriyaspielman:1234@cluster0-spfhl.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["firmware_data"]
    firmware_collection = db["firmware"]
    return firmware_collection


# check if the url exists and if the website has changed
def check_ur(collection, url , date):
    old_date = ""
    result = ""
    src = requests.get(url).text
    # parsing
    soup = BeautifulSoup(src, 'lxml')
    # if the document of the url exists
    if collection.find_one({"url": url}):
        result = collection.find({"url": url})
        # get the last modified from the database
        for a in result:
            old_date = a['build date']
        # if the website is modified - than update
        if old_date != date:
            get_data(soup, result)
        else:
            next_page(soup)
    # if the url data doesnt exists get the data (first run on that url)
    else:
        get_data(soup, result)


# get and insert the data
def get_data(soup, old_data):
    global data
    data = []
    # go over every product in the table
    for product in soup.find_all('tr', class_=['even', 'odd']):
        # extract and add device name
        name = product.a.text

        # extract version
        version = product.find('td', class_='views-field views-field-field-android-version2').text.strip()

        info = {
            'Device name': name,
            'Version': version
        }
        # if there is old data - check if the object already exists
        if old_data != "":
            for d in old_data:
                product_list = d['data']
        for p in product_list:
            # if the object is different - than insert
            if p != info:
                data.append(info)
        # if there is no data - insert all
        else:
            data.append(info)

    next_page(soup)


def next_page(soup):
    global new_url
    # check if we are not at the last page
    if soup.find('li', class_='pager-next last').find('a'):
        # update url for next page
        new_url = soup.find('li', class_='pager-next last').find('a')['href']
    else:
        # if we got to the last pagee - stop while lop
        new_url = "done"


def get_build_date(url):
    last_modified = ""
    header = requests.head(url).headers
    # get build date from page header
    if 'Last-Modified' in header:
        last_modified = header['Last-Modified']
    return last_modified


# save the url from input
baseUrl = sys.argv[1]
first_url = baseUrl + 'firmware-downloads'
data = []
build_date = get_build_date(first_url)
col = mongo_connection()
check_ur(col, first_url, build_date)
# if data is not empty - insert to database
if data:
    col.insert_one({'url': first_url, 'build date': build_date, 'data': data})

# go over all pages to get all the data
while new_url != "done":
    # request the new url
    build_date = get_build_date(baseUrl + new_url)
    curr_url = baseUrl + new_url
    check_ur(col, baseUrl + new_url, build_date)
# if data is not empty - insert to database
    if data:
        col.insert_one({'url': curr_url, 'build date': build_date, 'data': data})

