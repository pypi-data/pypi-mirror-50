# Dictsheet - Easy to use Google Spreadsheets Python API

Manage your spreadsheets in dict way. A easy to use Google spreadsheets Python API. Manage information in the sheet in rows. Based on gspread

Features:
* Manage the spreadsheet in dict way 
* Get/Set sheet mapping
* Update a row or element(s) in a row.
* Iterate rows in a spreadsheet.

## Requirements
Python 2.6+ or Python 3+, gspread

## Install

```sh
pip install dictsheet
```

## Basic Usage

1. [Obtain OAuth2 credentials from Google Developers Console](http://gspread.readthedocs.org/en/latest/oauth2.html)
2. Obtain the sheet title.
3. Start using dictsheet:
```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dictsheet import DictSheet

# The Credential file obtained from Google
CREDENTIAL_FILE = 'My Projecthah-xxxxxxx.json'
#Title of the sheet
SHEET_NAME = u'titleOfTheSheet'

# Create credentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_FILE, scope)
# Use gspread to connect to Google Spread Sheet
gc = gspread.authorize(credentials)
sh = gc.open(SHEET_NAME)
wks = sh.get_worksheet(0)


# Initialize dictsheet
dict_wks = DictSheet(wks=wks)

# Basic usage
# Get mapping
print dick_wks.mapping

# Set mapping
map = {"name":1, "phone":2, "address":3}
dict_wks.mapping = map

# Appending
dict_wks.append({"name": "Chandler Huang","phone": 987654321})

# Updating (2 is the row number)
dict_wks.update({2: {"name": "Kelly"}, 6:{"phone": 12345}})

# Iterating
for idx, dict_data in dict_wks.items():
    print idx, ' : ',dict_data

# Clearing a row
dict_wks[4].clear()
```



## Contributors

Chandler Huang, Xander Li

## Contact

previa@gmail.com, x@xanderli.com



