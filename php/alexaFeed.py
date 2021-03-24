#!/usr/bin/python
import websocket
import time
import base64
import json
import mysql.connector
from datetime import datetime
from subprocess import call



mydb = mysql.connector.connect(
    host="localhost",
    user="remote",
    password="PetFeeder2021!",
    database="Feeder",
)

dbcursor = mydb.cursor()
dbcursor.execute(
    "SELECT JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.sinricAPI')) as api, JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.sinricDeviceId')) as device FROM Feeder.Settings WHERE id = '1';"
)
dbresult = dbcursor.fetchone()

apiStr = "apikey:" + str(dbresult[0])
deviceStr = str(dbresult[1])
encoded_u = base64.b64encode(apiStr.encode()).decode()

def deviceAction(value, deviceName):
    if value == "ON":

        mydb = mysql.connector.connect(
            host="localhost",
            user="remote",
            password="PetFeeder2021!",
            database="Feeder",
        )

        dbcursor = mydb.cursor()
        dbcursor.execute(
            "SELECT JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.defaultFeedAmount')) as defaultFeedAmount FROM Feeder.Settings WHERE id = '1';"
        )
        dbresult = dbcursor.fetchone()
        print("alexa feed triggered: ")
        print("feed amount: ", float(dbresult[0]))
        sql = "INSERT INTO `Feeder`.`Logs` (`amount`, `trigger`) VALUES (%s, %s)"
        val = (dbresult[0], "alexa")
        dbcursor.execute(sql, val)
        mydb.commit()
        call(["python", "feed.py"])

def selectDevice(deviceId, action, value):
    if deviceId == deviceStr:  # Replace with your deviceId
        deviceAction(value, "Dog feeder")


def on_message(ws, message):
    obj = json.loads(message)
    deviceId = obj["deviceId"]
    action = obj["action"]
    value = obj["value"]
    selectDevice(deviceId, action, value)
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print
    "### closed ###"
    time.sleep(2)
    initiate()


def on_open(ws):
    print
    "### Initiating new websocket connection ###"


def initiate():
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        "ws://iot.sinric.com",
        header={"Authorization": "Basic %s" % encoded_u},
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open

    ws.run_forever()


if __name__ == "__main__":
    initiate()