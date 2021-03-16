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
```

## Configure mysql
```
sudo mysql_secure_installation
	You will be asked Enter current password for root (type a secure password): press Enter
	Type in Y and press Enter to Set root password
	Type in a password at the New password: prompt, and press Enter. Important: remember this root password, as you will need it later
	Type in Y to Remove anonymous users
	Type in Y to Disallow root login remotely
	Type in Y to Remove test database and access to it
	Type in Y to Reload privilege tables now
```

### edit mysql binded address (obtain your IP first)
```
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
-- change the IP to your own and save
bind-address            = 127.0.0.1

-- restart mysql
sudo service mysql restart
```

### Set your rpi hostname to petfeeder
```
sudo raspi-config
go to system options -> hostname 
set hostname to petfeeder and reboot
```

### Clone source code
```
cd ~/
sudo git clone https://github.com/drewklein20/dog-feeder.git
cd dog-feeder
```

### Build DB schema (in pet-feeder dir)
```
sudo mysql < schema.sql

sudo mysql

# Enter each command below
	USE FEEDER;
	CREATE USER 'remote'@'localhost' IDENTIFIED BY 'PetFeeder2021!';
	CREATE USER 'remote'@'%' IDENTIFIED BY 'PetFeeder2021!';
	GRANT ALL PRIVILEGES ON * . * TO 'remote'@'localhost';
	GRANT ALL ON *.* TO 'remote'@'%';
	FLUSH PRIVILEGES;
	exit;
```

### Build website (in pet-feeder dir)
```
sudo chmod +x build.sh
sudo ./build.sh
```
### Login/config
Go to http://petfeeder.local and login with username 'admin' and password 'password'

