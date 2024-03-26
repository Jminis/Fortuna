#!/bin/bash

read -p "Enter the name of the database: " database_name

export fortuna_database=$database_name

echo "The database name has been set to: $fortuna_database"

python make_database.py
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
