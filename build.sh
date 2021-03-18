#!/bin/bash

while getopts t: flag
do
    case "${flag}" in
        t) buildType=${OPTARG};;
    esac
done
echo "Build Type: $buildType";

echo "Building Pet Feeder";

echo -ne 'Creating DB schema';
sudo service mysql restart
sudo mysql -u root -pPetFeeder2021! < schema.sql

echo -ne 'Copying webserver files';
sudo rm -rf /var/www/html/*
sudo cp -r dist/* /var/www/html/
sudo mkdir /var/www/html/php
sudo cp -r php/* /var/www/html/php/
sudo chown -R www-data:www-data /var/www/
sudo usermod -aG www-data pi
addgroup www-data
sudo chown -R www-data:www-data /var/www/html/*
sudo chmod -R 770 /var/www/ /var/www/html/*

echo -ne 'Creating Alexa and Scale Services';
sudo rm /lib/systemd/system/scale.service
sudo rm /lib/systemd/system/alexa.service
sudo cp *.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/scale.service
sudo chmod 644 /lib/systemd/system/alexa.service
sudo chmod +x /var/www/html/php/scale.py
sudo chmod +x /var/www/html/php/feed.py
sudo chmod +x /var/www/html/php/alexaFeed.py
sudo systemctl daemon-reload
sudo systemctl enable alexa.service
sudo systemctl enable scale.service
sudo systemctl start alexa.service
sudo systemctl start scale.service
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

echo -ne 'Substituting hostname';
CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
# Hostname substitution
cd /var/www/html/

 ( shopt -s globstar dotglob;
     for file in **; do
         if [[ -f $file ]] && [[ -w $file ]]; then
             sed -i -- "s/feederhostname/${CURRENT_HOSTNAME}/g" "$file"
         fi
     done
 )
 echo "Finished!";