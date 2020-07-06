# GiftCardShop

Simple application of the online store, designed for selling giftcards of famous brands, based on **Django 3** and **Bootstrap 4**. 
An authorized user can add multiple giftcards with unique secret codes generated using uuid4. He can also edit and remove them.
An unauthenticated user can view the brands and associated gift cards, and add them to the cart. To make order user has to authenticate.
Since giftcard has reference to an order it's no longer available to buy. when the order is confirmed, a confirmation email is sent to the orders owner.
After successfull payment webhook from Stripe is received, a secret codes are sent in email to the customer. Email are sent by means of **Celery** async tasks with **Redis backend**.
If customer didn't payed his order in 3 days, it is marked as outdated and related giftcards become available to buy again. Restoring unpaid giftcards procedure is handled by **Celery beat schedule** everyday at 3 a.m.
Payments are handled by **Stripe.com**. User can pay only by card. 
Authorized user can make csv raport containing totals in choosen period of time, for one or few brands.

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
- make sure You have installed docker & docker-compose;
- clone this repo;
- make file ".env" in GiftcarShop folder and setup there environment variables as below ("Without docker") 
- cd into GiftcardShop and run -> docker-compose build;
- run ->  docker-compose up;
- in second terminal in GiftCardShop run -> docker exec -it web bash;
- then cd into giftcardshop;
- run -> python manage.py createsuperuser;
- provide admin account information;

For the experience of all features including webhooks, You should:
- make localhost tunnel (for example via **ngrok**) and add its https host to allowed hosts in giftcardshop/settings.py,
- add its host to webhook endpoints in Stripe (for example via dashboard)

Default localhosts:
- localhost:8000/admin/ -> admin site;
- localhost:8000/accounts/ -> generic django authentication views;
- localhost:8000/accounts/register/ -> registration view;
- localhost:8000/accounts/edit/ -> account edit view;
- localhost:8000/accounts/overview/ -> account history (list of past orders);
- localhost:8000/brands/list/<string:category>/ -> brand list view with optional category slug;
- localhost:8000/brands/<slug>/ -> brand detail view;
- localhost:8000/giftcards -> giftcards list view;
- localhost:8000/cart/add/ -> add to cart view;
- localhost:8000/cart/remove/<int:giftcard_id>/ -> remove from cart view;
- localhost:8000/cart/detail/ -> cart detail view;
- localhost:8000/orders/submit/ -> order create view;
- localhost:8000/orders/detail/<order_id>/ -> order detail view;
- localhost:8000/orders/delete/<order_id>/ -> order delete view;
- localhost:8000/orders/admin/raport/ -> raport creation view;
- localhost:8000/payments/checkout/<order_id>/ -> checkout view;
- localhost:8000/payments/webhook/ -> endpoint receiving Stripe's webhooks after successfull payment;
- localhost:8000/payments/success/ -> payment success view;
  










