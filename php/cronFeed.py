#!/usr/bin/env python2.7

import RPi.GPIO as GPIO
import time
import mysql.connector
from datetime import datetime
import pigpio
import time
import mysql.connector
import json
import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import os
pi = pigpio.pi() # Connect to local Pi.


# get the current time
now = datetime.now()
current_timestamp = now.strftime("%D %H:%M:%S")
current_time = now.strftime("%H:%M")

mydb = mysql.connector.connect(
  host="localhost",
  user="remote",
  password="PetFeeder2021!",
  database="Feeder"
)

dbcursor = mydb.cursor()
dbcursor.execute("SELECT * FROM Schedule")
dbresult = dbcursor.fetchall()

print("Timestamp: ", current_timestamp, " -Checking for scheduled feeds at: ", current_time)
for x in dbresult:
	if current_time == x[1]:
		print("time to feed")
		print("feed amount: ", float(x[2]))
		sql = "INSERT INTO `Feeder`.`Logs` (`amount`, `trigger`) VALUES (%s, %s)"
		val = (x[2], "scheduled feed")
		dbcursor.execute(sql, val)
		mydb.commit()
		execfile("/var/www/html/php/feed.py")
