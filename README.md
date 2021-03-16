# Pet Feeder

## Install required packages
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
## Give PHP permissions for python scripts
```
sudo visudo
```
At the bottom of this file, append the following line and save
```
www-data ALL=NOPASSWD: ALL
```

## Configure mysql
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


## Edit mysql binded address
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

## Set your rpi hostname to petfeeder (Don't skip this step, backend is setup to talk to this hostname)
```
sudo raspi-config
```
Go to system options -> hostname  
Set hostname to petfeeder and reboot  

## Clone source code
```
cd ~/
sudo git clone https://github.com/drewklein20/pet-feeder.git
cd pet-feeder
```

## Build DB schema (in pet-feeder dir)
```
sudo mysql < schema.sql
```
Then run (don't modify the username or password unless you plan on changing the source code)
```
sudo mysql
USE Feeder;
CREATE USER 'remote'@'localhost' IDENTIFIED BY 'PetFeeder2021!';
CREATE USER 'remote'@'%' IDENTIFIED BY 'PetFeeder2021!';
GRANT ALL PRIVILEGES ON * . * TO 'remote'@'localhost';
GRANT ALL ON *.* TO 'remote'@'%';
FLUSH PRIVILEGES;
exit;
```

## Build website (in pet-feeder dir)
```
sudo chmod +x build.sh
sudo ./build.sh
```
## Login/config
Go to http://petfeeder.local and login with username 'admin' and password 'password'

## Configuring Alexa
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

## Enable scheduler with cron
```
sudo crontab -e
```
Add the following line to the bottom
```
* * * * * sudo /usr/bin/python /var/www/html/php/cronFeed.py >> /var/www/html/php/cronLog.log 2>&1
```

## Set proper timezone
```
sudo raspi-config
```
Set your timezone under Localization Options (US central is what I used)



