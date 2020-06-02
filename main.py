from bs4 import BeautifulSoup
import requests
from datetime import date
import sys
#import pymongo


# get and insert the data
def get_data(source):
    soup = BeautifulSoup(source, 'lxml')  # parsing
    # go over every device
    for device in soup.find_all('tr', class_=['even', 'odd']):
        # extract and add device name
        name = device.a.text
        data['Device name'].append(name)

        # extract and add device version
        version = device.find('td', class_='views-field views-field-field-android-version2').text.strip()
        data['Version'].append(version)

        # add date
        today = date.today().strftime("%d/%m/%y")
        data['Build date'].append(today)

        # check if we are not at the last page
    if soup.find('li', class_='pager-next last').find('a'):
        global new_url
        # update url for next page
        new_url = soup.find('li', class_='pager-next last').find('a')['href']
    else:
        # if we got to the last pagee - stop while lop
        new_url = 0


data = {
    'Device name': [],
    'Version': [],
    'Build date': []
}
# save the url from input
baseUrl = sys.argv[1]
# go to downloads page for the data
src = requests.get(baseUrl + 'firmware-downloads').text
get_data(src)

# go over all pages to get all the data
while new_url != 0:
    # request the new url
    src = requests.get(baseUrl + new_url).text
    get_data(src)

print(data)
