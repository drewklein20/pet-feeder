# Raspberry PI Dog Feeder
This project was created with inspiration from Rob Peck's project (https://github.com/peckrob/petfeedd)  

## Features:
* Frontend created with vue.js and vuetify
* Schedule daily feeds
* See a log of feeds
* Trigger with Alexa
* Ability to integrate hx711 load cell for bowl weight (keeps from over feeding)
* Authentication

### 1.) Install required packages
```
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
sudo apt install apache2 -y
sudo apt install php -y
sudo apt install mariadb-server php-mysql -y
sudo apt install apache2 -y
sudo service apache2 restart
sudo apt install python3-pip -y
sudo apt install python-pip -y
sudo pip install install mysql-connector-python pigpio RPi.GPIO pysinric
sudo pip3 install hx711
sudo apt-get install pigpio
sudo pigpiod
```
### 2.) Give PHP permissions for python scripts
```
sudo visudo
```
At the bottom of this file, append the following line and save
```
www-data ALL=NOPASSWD: ALL
```

### 3.) Configure mysql
```
sudo mysql_secure_installation
```
You will be asked Enter current password for root (type a secure password): press Enter  
Type in Y and press Enter to Set root password  
Type in a password at the New password: prompt, and press Enter. Important: remember this root password, as you will need it later  
Type in Y to Remove anonymous users  
Type in N to Disallow root login remotely  
Type in Y to Remove test database and access to it  
Type in Y to Reload privilege tables now  


### 4.) Edit mysql binded address
```
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
Comment this line out with a #
```
bind-address            = 127.0.0.1
```
Restart mysql
```
sudo service mysql restart
```

### 5.) Set your rpi hostname to feeder (Don't skip this step, backend is setup to talk to this hostname)
```
sudo raspi-config
```
* Go to system options -> hostname  
* Set hostname to feeder and reboot  

### 6.) Clone source code
```
cd ~/
git clone https://github.com/drewklein20/pet-feeder.git
```

### 7.) Build DB and Webserver
```
cd pet-feeder
sudo chmod +x build.sh
sudo ./build.sh
```

### 8.) Login/config
Go to http://petfeeder.local and login with username 'admin' and password 'password'

### 9.) Configuring Alexa
* Log into the feeder and enable Alexa in the settings
* Go to https://sinric.com/ and create a free account
* Copy the sinric API key ("Your API Key") and save it in the feeder settings for Sinric API Key
* Create a new smart home device on the sinric site (device type: switch)
* Copy the deviceId and save it in the feeder settings for Sinric DeviceId
* Save the settings in the app

* In the alexa app, add the sinric skill, then discover devices
* Create a new routine that turns on the device you just created (don't worry about turning off)
* Test the routine on your alexa device and verify the feeder runs

To debug, run sudo python /var/www/html/php/alexaFeed.py (If configured correctly, you should see text logged when Alexa is triggered)

### 10.) Enable scheduler with cron
```
sudo crontab -e
```
Add the following line to the bottom
```
* * * * * sudo /usr/bin/python /var/www/html/php/cronFeed.py >> /var/www/html/php/cronLog.log 2>&1
```

### 11.) Set proper timezone
```
sudo raspi-config
```
Set your timezone under Localization Options (US central is what I used)

### 12.) Calibrating scale
* First in the app settings, enable the scale and save.  
* Find an object that you know the exact weight of in grams or kg (I used an echo dot & I googled the weight)  
* cd into the pet-feeder directory and run the following (you should see values being output)
```
sudo python scale-example.py
```
* Now add the object to the scale and observe the new values. 
* If the values are somewhat consistent, take one and divide it by your object's weight in kg). This value will be your reference unit.
* Now edit the scale-example.py file and uncomment the following line and set it to your reference unit value.
```
#referenceUnit = 160
```
* Remove the weight and rerun the example file and verify your numbers are closer to 0. Then apply the weight and verify you are seeing correct numbers.
* If you are seeing the correct numbers, change the reference unit in the app settings and save.
* If you are seeing very random values the following was helpful to me
  * verify all soldering was done correctly
  * change the first parameter to "LSB" for the following line in the scale-example.py file
    ```
    hx.set_reading_format("MSB", "MSB")
    ```




