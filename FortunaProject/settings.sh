#!/bin/bash
sudo apt update
sudo apt upgrade
sudo apt install redis-server
sudo apt install pkg-config
sudo apt install python3-dev default-libmysqlclient-dev build-essential
sudo apt install mysql-server
sudo apt install mysqlclient
pip install django_celery_beat
pip install whitenoise

sudo systemctl start mysql.service

echo "Enter password for MySQL root user:"
read -s rootpasswd

sudo mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql -u root -p mysql
sudo mysql -u root -p$rootpasswd <<MYSQL_SCRIPT
CREATE DATABASE fortuna;
CREATE USER 'fortuna'@'localhost' IDENTIFIED BY 'fortuna';
GRANT ALL PRIVILEGES ON fortuna.* TO 'fortuna'@'localhost';
SET time_zone='Asia/Seoul';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

echo "MySQL database created."
echo "Username:   fortuna"
echo "Password:   fortuna"
