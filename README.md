# Blog-API 📃

Blog-Api made with django rest-framework

This a simple Blog posting API

Users can like and dd comment to thr plog posts

User's can create-account / login / logout / resetpassword / changepassword

## Authentication 🔐

A ***custom User model*** was used for users in blog 

For authentication used django-rest-auth

Users can change pass word / resret password 

All login / logout / etc are ***token based authentication***

## How The API works

For Api doc


## How use Blog-API 🤔

First install the requirements.txt:

    pip install -r requirements.txt

Then set your Database config and run:

    python manage.py makemigrations && python manage.py migrate

