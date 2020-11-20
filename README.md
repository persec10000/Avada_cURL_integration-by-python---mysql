# Avada_cURL_integration-by-python---mysql

pycurl install
	https://stackoverflow.com/questions/53492993/pycurl-installation-on-python-3-7-0-windows-10
	https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl
	
	C:\d>python --version
	Python 3.8.3
	C:\d>pip install C:/d/pycurl-7.43.0.4-cp38-cp38-win32.whl
	pip install mysql-connector-python
	pip install mysql-client
	
===================

Simple python script to retrieve data from API and then saving to DB.

Documentation for API https://api.avaza.com/swagger/ui/index#!/Timesheet/Timesheet_Get
Only call that are needed is GET /api/TimeSheet

Library to use for connecting to DB:
import mysql.connector

Script need to be able to run with:
if __name__ == '__main__':
date_start = '2020-10-01'
date_end = '2020-10-27'
main_script(date_start, date_end)


--------------------

Her is the API Tooken:
254577-8a4ec5a32fcbf07c7c3c26da30232ab917495f2a
254577-8a4ec5a32fcbf07c7c3c26da30232ab917495f2a

Example Curl:
curl -X GET --header 'Accept: application/json' --header 'Authorization: Bearer 254578-3344396584277ffe7196921ae74444ff2db6556f' 'https://api.avaza.com/api/Timesheet?EntryDateFrom=2020-10-01&EntryDateTo=2020-10-20'

Request URL
https://api.avaza.com/api/Timesheet?EntryDateFrom=2020-10-01&EntryDateTo=2020-10-20
is hten giving:
"TotalCount": 433,
"PageNumber": 1,
"PageSize": 20
** is then returning

