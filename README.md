# Web_Crawler
Implement a web crawler in Python that browses a vendor website, downloads firmware files, and fetches their metadata. 

Run command : python3 main.py https://www.rockchipfirmware.com/

The data is saved in MongoDB.
Each document contains:
-
-Url
-Build date
-Array of objects, each object contains:
  *Device name
  *Version
