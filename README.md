# GiftCardShop

Simple application of the online store, designed for selling giftcards of famous brands, based on **Django 3** and **Bootstrap 4**. 
An authorized user can add multiple giftcards with unique secret codes generated using uuid4. He can also edit and remove them.
An unauthenticated user can view the brands and associated gift cards, and add them to the cart. To make order user has to authenticate.
Since giftcard has reference to an order it's no longer available to buy. 
Payments are handled by **Stripe.com**. User can pay only by card. 
Authorized user can make csv raport containing totals in choosen period of time for one or few brands.

Steps to setup application:

Without docker:
- clone this repo;
- make virtual environment and install all dependencies listed in Pipfile or requirements.txt,
- setup environment variables in your virtual environment as follows: STRIPE_PUBLISHABLE_KEY='your key';STRIPE_SECRET_KEY='your key'; EMAIL_HOST='your email host'; EMAIL_HOST_USER='your email user';   EMAIL_HOST_PASSWORD='your email password'; EMAIL_PORT= your email port default: 587;
- activate virtualenv;
- migrate db;
- create super user;
- run python manage.py runserver

With docker:
- make sure You have installed docker-compose;
- clone this repo;
- cd into GiftcardShop and run docker-compose up










