# django-chat
My attempt at using REST API and Django database back-end to make a chat app.
## Prerequisites
Make sure you have these modules installed in your enviroment:
 - Twisted             18.7.0
 - psycopg2-binary     2.7.5
 - Pillow              5.2.0
 - django-rest-auth    0.9.3
 - djangorestframework 3.8.2
 - Django              2.0.7
 - daphne              2.2.0
 - channels            2.1.2
 - channels-redis      2.2.1
## Installation
This repository does not contain `settings.py` because of configuration privacy, but does contain example file `example_settings.py`. You need to set it up by to work with `Django`, `Django REST Framework` and `Django Channels`.
`Pillow` is required to handle users' avatars.

After cloning this repository, before first migration, plase change the content of `main.models.py`, from:
```
usercode = models.CharField(default=create_profile_usercode,
                                max_length=100)
```
to:
```
usercode = models.CharField(default="somedir/",
                                max_length=100)
```
After the initial migration please change `default` to the original value and make another migration. This is because `user_directory_path(instance, filename)` function which dynamically generates media dir for each respective user doesn't quite work with custom `User` model.
After that you should be done and no additional tweaks should be needed. In case some module is missing, please check if you have all packages required by `Django`, `Django Channels` or `Django REST Framework`. 
## Usage
This app works in a pretty simple way. Each newly registered `User` is given unique `usercode` generated on account creation. It is later on used to identify the user in many different ways and allows communication between them. App is equipped with fully functional REST API that allows for sending messages, retrieving them and many more. Apart from registration, every of API views is authenticated by a Token.
The Chat is divided into `main` and `api` modules. `api` contains the REST API, but `main` contains the web chat client. It uses WebSocket to receive live chat updates and uses Javascript AJAX calls to use the API.
