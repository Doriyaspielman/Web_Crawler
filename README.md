# Web_Crawler
Implement a web crawler in Python that browses a vendor website, downloads firmware files, and fetches their metadata. 
 
## How to use?
Run command:
```bash
python3 main.py https://www.rockchipfirmware.com/
```

## Database
The data is store in MongoDB. <br />
Each document contains: <br />
* Url
* Build date
* Array of objects, each object contains:
  * Device name
  * Version

## Technologies
Project is created with:
* Python3 version: 3.8.2
* requests library
* Beautiful Soup library
* pyMongo library
