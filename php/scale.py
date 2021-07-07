#! /usr/bin/python2.7

import time
import sys
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="remote",
    password="PetFeeder2021!",
    database="Feeder"
)

dbcursor = mydb.cursor()
dbcursor.execute("SELECT JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.isUsingScale')) as isUsingScale, JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.scaleReferenceUnit')) as referenceUnit FROM Feeder.Settings;")
dbresult = dbcursor.fetchone()

if dbresult[0] == 'true':
    referenceUnit = int(dbresult[1])

    previousWeight = 0
    EMULATE_HX711 = False

    print("starting scale")

    if not EMULATE_HX711:
        import RPi.GPIO as GPIO
        from hx711 import HX711
    else:
        from emulated_hx711 import HX711

    def cleanAndExit():
        print("Cleaning...")

        if not EMULATE_HX711:
            GPIO.cleanup()

        print("Bye!")
        sys.exit()

    hx = HX711(5, 6)

    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()

    while True:
        try:
            value = hx.get_weight(5)
            print(value)
            diff = abs(value) - abs(previousWeight)

            if abs(diff) > 15:
                print("weight change detected: ", value)
                sql = "INSERT INTO `Feeder`.`scaleWeights` (`value`) VALUES ('" + \
                    str(value) + "')"
                dbcursor.execute(sql)
                mydb.commit()

            previousWeight = value
            hx.power_down()
            hx.power_up()
            time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
