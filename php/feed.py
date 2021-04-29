#!/usr/bin/env python2.7

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
pi = pigpio.pi()  # Connect to local Pi.


# ---- gmail send email ----------
def send_email(emailConfig, petName, feedCups, trigger, cameraEnabled):
    gmail_user = emailConfig["proxyEmail"]
    gmail_password = emailConfig["proxyPassword"]
    port = int(emailConfig["port"])
    sent_from = emailConfig["proxyEmail"]

    toEmails = emailConfig["toEmail"].split(",")

    for toEmail in toEmails:
        mail_content = """Your pet was fed!"""
        message = MIMEMultipart()
        message['From'] = gmail_user
        message['To'] = toEmail
        message['Subject'] = 'PetFeeder Alert'

        # &petname& &feedCups&
        html = """\
		<!DOCTYPE html><html lang="en"><head>  <title>PetFeeder Alert</title>  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  <meta name="viewport" content="width=device-width, initial-scale=1" />  <meta http-equiv="X-UA-Compatible" content="IE=edge" />  <style type="text/css">    /* CLIENT-SPECIFIC STYLES */    body,    table,    td,    a {      -webkit-text-size-adjust: 100%;      -ms-text-size-adjust: 100%;    }    table,    td {      mso-table-lspace: 0pt;      mso-table-rspace: 0pt;    }    img {      -ms-interpolation-mode: bicubic;    }    /* RESET STYLES */    img {      margin-top: 60px;      border: 0;      height: auto;      line-height: 100%;      outline: none;      text-decoration: none;    }    table {      border-collapse: collapse !important;    }    body {      height: 100% !important;      margin: 0 !important;      padding: 0 !important;      width: 100% !important;    }    /* MAIN CSS */    a {      color: #0E1C36 !important;      font-weight: 500;      text-decoration: none !important;    }    a:-webkit-any-link {      text-decoration: none !important;      color: #0E1C36 !important;    }    a:hover {      text-decoration: none !important;    }    strong {      color: black !important;    }    p {      color: black !important;    }    li {      color: black !important;    }    hr {      margin-top: 40px;      margin-bottom: 40px;    }    .center {      text-align: center !important;    }    .login {      color: #0E1C36;      text-decoration: none;      margin-top: 30px;      margin-bottom: 30px;    }    .thanks {      color: #212121;      margin-bottom: 30px;      margin-top: 30px;    }    .notice {      color: #0E1C36 !important;      font-size: small;      line-height: 18px !important;    }    .foot {      max-width: 800px;      margin: auto;    }    @media screen and (min-width: 600px) {      h1 {        font-size: 32px !important;        line-height: 48px !important;      }      .intro {        font-size: 24px !important;        line-height: 36px !important;      }      .main-body {        padding: 24px 48px !important;      }    }  .center-img { display: block; margin-left: auto; margin-right: auto; width: 60%; }</style></head><body style="margin: 0 !important; padding: 0 !important;">  <div style="display: none; max-height: 0px; overflow: hidden;">Your pet has been fed!</div>  <div style="display: none; max-height: 0px; overflow: hidden;">    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;  </div>  <!-- This ghost table is used to constrain the width in Outlook. The role attribute is set to presentation to prevent it from being read by screenreaders. -->  <!--[if (gte mso 9)|(IE)]>    <table cellspacing="0" cellpadding="0" border="0" width="600" align="center" role="presentation"><tr><td>    <![endif]-->  <div role="article" aria-label="PetFeeder Alert" lang="en" style="        background-color: white;        color: #AFCBFF;        font-family: " Avenir Next", -apple-system, BlinkMacSystemFont, "Segoe UI" , Roboto, Helvetica, Arial,    sans-serif, "Apple Color Emoji" , "Segoe UI Emoji" , "Segoe UI Symbol" ; font-size: 18px; font-weight: 400;    line-height: 28px; margin: 0 auto; max-width: 600px; padding: 40px 20px 40px 20px; "    >      <header>          <center>           </center>        <h1 style="                color: #0E1C36;                font-size: 32px;                font-weight: 400;                line-height: 32px;                margin: 48px 0;                text-align: center;                font-family: Open Sans, Helvetica, Arial, sans-serif;              ">            PetFeeder Alert        </h1>     </header>  <main>    <div class="main-body" style="    background-color: #AFCBFF;    border-radius: 4px;    padding: 24px 24px;    max-width: 800px;    margin: auto;  ">      <!-- This ghost table is used solely for padding in Word-based Outlook clients. -->      <!--[if (gte mso 9)|(IE)]>                <table cellspacing="0" cellpadding="0" border="0" width="600" align="center" role="presentation"><tr><td style="background-color: ghostwhite;font-family: "Avenir Next", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; padding: 24px 48px 24px 48px;">                <![endif]-->      <p style="font-family: Open Sans, Helvetica, Arial, sans-serif;">        You have successfully fed &petname& &feedCups& of food!  &trigger&    </p>    <img class="center-img" src="cid:0">    <hr />         <p class="center" style="font-family: Open Sans, Helvetica, Arial, sans-serif; text-align: center!important;">       Thank you for using PetFeeder!      </p>      <p class="center"       style="text-align: center!important; font-family: Open Sans, Helvetica, Arial, sans-serif; text-decoration: none !important; color: #0E1C36 !important; text-align: center!important; overflow-wrap: anywhere;word-break:break-all;"> </p>         <!--[if (gte mso 9)|(IE)]>                </td></tr></table>                <![endif]-->    </div>  </main>  <footer>    <div class="foot main-body" style="padding: 24px 24px;">   </div>  </footer>  </div>  <!--[if (gte mso 9)|(IE)]>    </td></tr></table>    <![endif]--></body></html>
		"""
        triggerText = ""
        if trigger == "app":
            triggerText = "This feed was triggered by the app."
        elif trigger == "scheduled feed":
            triggerText = "This was a scheduled feed."
        elif trigger == "alexa":
            triggerText = "This feed was triggered by Alexa."

        cupText = str(feedCups) + " cups"
        if str(feedCups) == "1":
           cupText = str(feedCups) + " cup"


        html = html.replace("&petname&", petName)
        html = html.replace("&trigger&", triggerText)
        html = html.replace("&feedCups&", cupText)
        part1 = MIMEText(html, 'html')
        message.attach(part1)

        if cameraEnabled:
            # to add an attachment is just add a MIMEBase object to read a picture locally.
            with open('/var/www/html/php/cam/live.jpg', 'rb') as f:
                # set attachment mime and file name, the image type is png
                mime = MIMEBase('image', 'jpg', filename='live.jpg')
                # add required header data:
                mime.add_header('Content-Disposition',
                                'attachment', filename='live.jpg')
                mime.add_header('X-Attachment-Id', '0')
                mime.add_header('Content-ID', '<0>')
                # read attachment file content into the MIMEBase object
                mime.set_payload(f.read())
                # encode with base64
                encoders.encode_base64(mime)
                # add MIMEBase object to MIMEMultipart object
                message.attach(mime)

        text = message.as_string()

        try:
            if (emailConfig["ssl"] == True):
                server = smtplib.SMTP_SSL('smtp.gmail.com', port)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, toEmail, text)
                server.close()
            else:
                server = smtplib.SMTP('smtp.gmail.com', port)
                server.starttls()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, toEmail, text)
                server.close()
            print 'Email sent!'
        except:
            print 'Something went wrong...'


# ---- main feed function --------
def feed():
    mydb = mysql.connector.connect(
        host="localhost",
        user="remote",
        password="PetFeeder2021!",
        database="Feeder"
    )

    currentWeight = 0
    fullBowlWeight = 100

    dbcursor = mydb.cursor()
    dbcursor.execute("SELECT preferences FROM Feeder.Settings;")
    dbresult = dbcursor.fetchone()
    preferences = json.loads(dbresult[0])

    cupDuration = preferences["cupDuration"]
    speedSetting = preferences["speed"]
    speed = 2000

    if speedSetting == "1":
        speed = 1600
    if speedSetting == "2":
        speed = 1650
    if speedSetting == "3":
        speed = 1700
    if speedSetting == "4":
        speed = 1750
    if speedSetting == "5":
        speed = 1800
    if speedSetting == "6":
        speed = 1850
    if speedSetting == "7":
        speed = 1900
    if speedSetting == "8":
        speed = 1950
    if speedSetting == "9":
        speed = 2000

    emailNotifications = preferences["emailNotifications"]
    cameraEnabled = preferences["isUsingCamera"]
    emailConfig = preferences["emailConfig"]
    isIncrementFeed = preferences["isIncrementFeed"]
    twoBowls = preferences["twoBowls"]
    leftBowlOffset = preferences["leftBowlOffset"]
    rightBowlOffset = preferences["rightBowlOffset"]
    isUsingScale = preferences["isUsingScale"]
    petName = preferences["petName"]

    if isUsingScale:
        fullBowlWeight = preferences["fullBowlWeight"]

        dbcursor = mydb.cursor()
        dbcursor.execute(
            "SELECT * FROM Feeder.Weights order by id desc limit 1;")
        dbresult = dbcursor.fetchone()
        currentWeight = dbresult[1]

    dbcursor = mydb.cursor()
    dbcursor.execute("SELECT * FROM Logs ORDER BY id desc LIMIT 1")
    dbresult = dbcursor.fetchone()
    feedCups = dbresult[2]
    trigger = dbresult[3]

    cumulativeTime = 0.0
    feedAmount = float(cupDuration) * float(feedCups)

    if isIncrementFeed:
        # Change the feed amount if incrementFeed (cupDuration becomes number of pulses)
        feedAmount = (float(cupDuration) * 0.10) * float(feedCups)

    if currentWeight < fullBowlWeight:
        try:
            if isIncrementFeed:
                while cumulativeTime < feedAmount:
                    feedAmount = feedAmount + float(rightBowlOffset)
                    pi.set_servo_pulsewidth(17, speed)
                    time.sleep(0.10)
                    pi.set_servo_pulsewidth(17, 0)
                    time.sleep(0.30)
                    cumulativeTime += 0.10
            else:
                    feedAmount = feedAmount + float(rightBowlOffset)
                    pi.set_servo_pulsewidth(17, speed)
                    time.sleep(feedAmount)
                    pi.set_servo_pulsewidth(17, 0)
                if twoBowls:
                    time.sleep(1)
                    feedAmount = feedAmount + float(leftBowlOffset)
                    pi.set_servo_pulsewidth(17, 1000)
                    time.sleep(feedAmount)
                    pi.set_servo_pulsewidth(17, 0)
            pi.stop()

        except KeyboardInterrupt:
            GPIO.cleanup()

    if cameraEnabled == True:
        print("taking pic")
        os.system(
            "sudo raspistill -w 1944 -h 2592 -rot 90 -vf -hf -o /var/www/html/php/cam/live.jpg")

    if emailNotifications == True:
        print("sending email")
        send_email(emailConfig, petName, feedCups, trigger, cameraEnabled)


# call main feed function
feed()