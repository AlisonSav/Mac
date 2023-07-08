# Mac

<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">This is Mac-Restaurant project!</h3>
Overview
This web application creates an online catalog for restaurant management, where users can browse available restaurants and manage information.

The main features that have currently been implemented are:

There are models for Restaurants, restaurant's Area, Dishes and Products.
Users can view list and detail information for all models.
Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).

Quick Start
To get this project up and running locally on your computer:

Set up the Python development environment. We recommend using a Python virtual environment.
Assuming you have Python setup, run the following commands (if you're on Windows you may use py or py -3 instead of python to start Python):
pip3 install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py collectstatic
py manage.py test # Run the standard tests. These should all pass.
py manage.py createsuperuser # Create a superuser
py manage.py runserver
to run tests:
tox run all tests (flake8, black, unittests)
tox -epep8 run flake8 tests
tox -eblack run black diff tests
tox -etest run only unittests
Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
Create a few test objects of each type.
Open tab to http://127.0.0.1:8000 to see the main site, with your new objects.
If you to create some objects - you need
- first create Areas -py manage.py create_area int
- after create Restaurants, because this model has O2O relations with Area model -py manage.py create_restaurant int(1, 11)
- create Dish(FK - Restaurant, M2M with Product) -py manage.py create_restaurant int
- create Product -py manage.py create_product int
- create Relations for Dish-Product -py manage.py create_product_dish_relations int
