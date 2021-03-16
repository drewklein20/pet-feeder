#!/usr/bin/env python2.7

import pigpio
import time
import mysql.connector
pi = pigpio.pi() # Connect to local Pi.

mydb = mysql.connector.connect(
  host="localhost",
  user="remote",
  password="PetFeeder2021!",
  database="Feeder"
)

isUsingScale = False
twoBowls = False
currentWeight = 0
fullBowlWeight = 0

dbcursor = mydb.cursor()
dbcursor.execute("SELECT JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.cupDuration')) as cupDuration, JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.bowlWeight')) as cupDuration, JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.twoBowls')) as twoBowls, JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.isUsingScale')) as isUsingScale FROM Feeder.Settings;")
dbresult = dbcursor.fetchone()
cupDuration = dbresult[0]

if dbresult[2] == 'true':
	twoBowls = True
if dbresult[3] == 'true':
	isUsingScale = True
	fullBowlWeight = dbresult[1]

	dbcursor = mydb.cursor()
	dbcursor.execute("SELECT * FROM Feeder.Weights order by id desc limit 1;")
	dbresult = dbcursor.fetchone()
	currentWeight = dbresult[1]

dbcursor = mydb.cursor()
dbcursor.execute("SELECT * FROM Logs ORDER BY id desc LIMIT 1")
dbresult = dbcursor.fetchone()
feedCups = dbresult[2]

print(twoBowls)
print(currentWeight)
print(fullBowlWeight)

sleepAmount = float(cupDuration) * float(feedCups)

if currentWeight < fullBowlWeight:
	try:
		pi.set_servo_pulsewidth(17, 2000)
		time.sleep(sleepAmount)
		# switch servo off
		pi.set_servo_pulsewidth(17, 0);
		if twoBowls:
			time.sleep(1)
        	        pi.set_servo_pulsewidth(17, 1000)
               		time.sleep(sleepAmount)
                	pi.set_servo_pulsewidth(17, 0)
		pi.stop()

	except KeyboardInterrupt:
        	GPIO.cleanup()