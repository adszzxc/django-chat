# django-chat
My attempt at using REST API and Django database back-end to make a chat app.

This web app consits of essentially three models: Profile, Chat and Message. 
Each Profile is linked by `OneToOneField` with `django.contrib.auth.models.User` object. Sending messages and other interactions can be done by REST API provided, authenticated by a Token. 

Each user has unique `usercode` string that is used to identify the profile and send messages to that `Profile` as nicknames can change but `usercode` will always be the same. When connecting to the Websocket, an authenticated user gets added to a group named by that `Profile`'s usercode so clients on multiple devices can be used. In order to access the API, you need to make a POST request to `/api/auth/login/` with `User` username and password as POST data. Then set the returned Token as a header like `{"Authorization":"Token your_token"}`.

# packages
- PIL 5.2.0
- Channels 2.1.2
- Daphne 2.2.0
- Twisted 18.4.0
- Django 2.0.7
- Python 3.5.2
- redis-cli 3.0.6
