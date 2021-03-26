#!/bin/bash


read -p "Full build (y/n)?" choice
case "$choice" in 
  y|Y ) fullBuild=true;;
  n|N ) fullBuild=false;;
  * ) echo "invalid";;
esac


echo "Building Compu-Feed";

if [ "$fullBuild" = true ] ; then
    echo  'Creating DB schema';
    sudo service mysql restart
    sudo mysql -u root -pPetFeeder2021! < schema.sql
fi

echo  'Copying webserver files';
sudo rm -rf /var/www/html/*
sudo cp -r dist/* /var/www/html/
sudo mkdir /var/www/html/php
sudo cp -r php/* /var/www/html/php/
sudo chown -R www-data:www-data /var/www/

if [ "$fullBuild" = true ] ; then
    sudo usermod -aG www-data pi
    addgroup www-data
fi

sudo chown -R www-data:www-data /var/www/html/*
sudo chmod -R 770 /var/www/ /var/www/html/*

if [ "$fullBuild" = true ] ; then
    echo  'Creating Alexa and Scale Services';
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
fi

echo  'Substituting hostname';
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
 echo -e "\e]8;;http://${CURRENT_HOSTNAME}.local\ahttp://${CURRENT_HOSTNAME}.local\e]8;;\a"

if [ "$fullBuild" = true ] ; then
    echo "Username: admin";
    echo "Password: password";
fi