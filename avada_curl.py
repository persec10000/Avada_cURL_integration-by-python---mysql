from io import BytesIO 
import mysql.connector
import requests
import json


def main_script(date_start,date_end):
	headers = {
	    'Accept': 'application/json',
	    'Authorization': 'Bearer 254578-3344396584277ffe7196921ae74444ff2db6556f',
	}

	params = (
	    ('EntryDateFrom', date_start),
	    ('EntryDateTo', date_end),
	    ('pageSize', "1000"),
	)

	response = requests.get('https://api.avaza.com/api/Timesheet', headers=headers, params=params)

	file = open("resp_text.txt", "w")
	file.write(response.text)
	file.close()


	#------------------------------------
	#print (response.content)

	# mysql db
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  password=""
	)

	mycursor = mydb.cursor()
	mycursor.execute("SHOW DATABASES")
	isDbExist = 0
	mydbname="dbavaza"
	for x in mycursor:
	  print(x)
	  if mydbname in x:
	  	isDbExist = 1
	  	
	if isDbExist==1:
		print ("-- DB is already created.")
	else:
		print ("-- DB is newly created.")
		mycursor.execute("CREATE DATABASE dbavaza")

	mycursor.execute("USE dbavaza")
	mycursor.execute("SHOW TABLES")
	isTblExist = 0
	mytblname="avaza_timesheet"
	for x in mycursor:
	  print(x)
	  if mytblname in x:
	  	isTblExist = 1
	if isTblExist==1:
		print ("-- Tbl is already created.")
	else:
		print ("-- Tbl is newly created.")
		#mycursor.execute("CREATE TABLE tblcustomers \
		# (name VARCHAR(255), address VARCHAR(255))")

		mycursor.execute("CREATE TABLE avaza_timesheet (\
			timesheet_entry_id int(10) unsigned NOT NULL,\
			user_idfk int(11) DEFAULT NULL,\
			firstname varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,\
			lastname varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,\
			project_idkf int(11) DEFAULT NULL,\
			project_title varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,\
			customer_idkf int(11) DEFAULT NULL,\
			customer_name varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,\
			timesheet_category_idkf int(11) DEFAULT NULL,\
			category_name varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,\
			duration double DEFAULT NULL,\
			entry_date datetime DEFAULT NULL,\
			avaza_timesheetcol varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,\
			notes text COLLATE utf8mb4_unicode_ci,\
			task_idkf int(11) DEFAULT NULL,\
			task_title varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,\
			date_created datetime DEFAULT NULL,\
			date_updated datetime DEFAULT NULL,\
			PRIMARY KEY (timesheet_entry_id),\
			UNIQUE KEY timesheet_entry_id_UNIQUE (timesheet_entry_id)\
			) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")



	with open('resp_text.txt') as f:
	  data = json.load(f)

	print(data["TotalCount"]) 
	if data["TotalCount"] > 1000 :
		print ("Error:TotalCount is over than 1000")
		return



	sql = "INSERT INTO avaza_timesheet (timesheet_entry_id, user_idfk, firstname, lastname, project_idkf,project_title,\
		customer_idkf,customer_name,timesheet_category_idkf,category_name,duration,\
		entry_date,avaza_timesheetcol,notes,task_idkf,task_title,date_created,date_updated)\
		 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
	for rowJson in data["Timesheets"]:
		fldID = rowJson["TimesheetEntryID"]
		fldUserIDFK = rowJson["UserIDFK"]
		fldFirstname = rowJson["Firstname"]
		fldLastname = rowJson["Lastname"]
		fldProjectIDFK = rowJson["ProjectIDFK"]
		fldProjectTitle = rowJson["ProjectTitle"]
		fldCustomerIDFK = rowJson["CustomerIDFK"]
		fldCustomerName = rowJson["CustomerName"]
		fldTimesheetCategoryIDFK = rowJson["TimesheetCategoryIDFK"]
		fldCategoryName = rowJson["CategoryName"]
		fldDuration = rowJson["Duration"]
		fldEntryDate = rowJson["EntryDate"]
		fldAvaza_timesheetcol = " "
		fldNotes = rowJson["Notes"]
		fldTaskIDFK = rowJson["TaskIDFK"]
		fldTaskTitle = rowJson["TaskTitle"]
		fldDateCreated = rowJson["DateCreated"]
		fldDateUpdated = rowJson["DateUpdated"]
		valIns = (fldID,fldUserIDFK,fldFirstname,fldLastname,fldProjectIDFK,fldProjectTitle,fldCustomerIDFK,fldCustomerName,fldTimesheetCategoryIDFK,fldCategoryName,fldDuration,fldEntryDate,fldAvaza_timesheetcol,fldNotes,fldTaskIDFK,fldTaskTitle,fldDateCreated,fldDateUpdated)	
		valUdt = (fldUserIDFK,fldFirstname,fldLastname,fldProjectIDFK,fldProjectTitle,fldCustomerIDFK,fldCustomerName,fldTimesheetCategoryIDFK,fldCategoryName,fldDuration,fldEntryDate,fldAvaza_timesheetcol,fldNotes,fldTaskIDFK,fldTaskTitle,fldDateCreated,fldDateUpdated,fldID)	
		try:
			mycursor.execute(sql, valIns)
			print ("Field is inserted.")
		except:		
			mycursor.execute ("""UPDATE avaza_timesheet
				SET user_idfk=%s, firstname=%s, lastname=%s, project_idkf=%s,project_title=%s,customer_idkf=%s,customer_name=%s,timesheet_category_idkf=%s,category_name=%s,duration=%s,entry_date=%s,avaza_timesheetcol=%s,notes=%s,task_idkf=%s,task_title=%s,date_created=%s,date_updated=%s
				WHERE timesheet_entry_id=%s""", valUdt)
			print ("Field is updated.")	

		mydb.commit()

		#print(mycursor.rowcount, "record inserted.")


if __name__ == '__main__':
	date_start = '2020-10-21'
	date_end = '2020-10-28'
	main_script(date_start,date_end)