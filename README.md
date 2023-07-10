
Simple Blog-Api made with django rest-framework Done in 1 day

Users can like and add comment to plog posts

User's can create-account / login / logout / resetpassword / changepassword

## Authentication 🔐

A ***custom User model*** was used for users in blog 

For authentication used django-rest-auth

Users can change pass word / resret password 

All login / logout / etc are ***token based authentication***

## How The API works 

Authenticated Users can create Posts 

Only the **post author** can __Edit or Delete__ the post

Users can add __up to 3 Comments__

Users can **Like or DisLike Blog posts**

Posts show the **list of comments** and the user of the comments AND **like and dislike count**

For Api documentation used **swagger and redoc**

Both are available in /swagger/ or /redoc/

Custom User accounts Handeling is available in /accounts/

posts CRUD is available in /post/

## Swagger Shema 

![252020734-ef3a4f81-56e9-49a8-85d7-47cb0fb3672a](https://github.com/Arshia-Izadyar/adv-Blog-API/assets/110552657/a92d9df2-6dd8-41b7-87ea-985860d7d26b)



## How use Blog-API 🤔

First install the requirements.txt:

    pip install -r requirements.txt

Then set your Database config and run:

    python manage.py makemigrations && python manage.py migrate

