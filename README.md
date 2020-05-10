# Restaurants Catalog

Restaurants Catalog is a web application that provides a list of restaurants with different menu items. 

It integrates third party user registration and authentication. Authenticated users have the ability to create, edit, and delete their own restaurants and menus.

This is my project for the [Udacity's Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) courses [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) and [Authentication & Authorization: OAuth](https://www.udacity.com/course/authentication-authorization-oauth--ud330).

You can view all of my Nanodegree projects from this repo [mohllal/udacity-fsnd](https://github.com/mohllal/udacity-fsnd).

### Prerequisites:
The application was built using [Python 2.7](https://www.python.org/downloads/).
It used [SQLite](https://www.sqlite.org/) as the underlying database technology.
The application uses [Flask](http://flask.pocoo.org/) framework and [SQLAlchemy](https://www.sqlalchemy.org/) toolkit so you should ensure you have them installed on your machine.

### Features:
- User registration system.
- Authentication using Google's authentication service.
- CRUD Restaurant operations.
- CRUD Menu operations.
- Review (rate and comment) to other menus.
- JSON API endpoints for all restaurants, menus, and reviews.
- CRUD images operations: An image can be added for each restaurant or menu. This can be done by uploading a local file and if no image is added, a default image is shown.
- Secure against Cross-Site Request Forgery (CSRF) attacks.
- Elegant UI.

### Files:
- **`app.py`**: This file contains the whole server side programming logic of the application.
- **`models.py`**: Contains the database model and is used to create the initial database.
- **`restaurantmenu.db`**: Database file containing some example restaurants, menus and reviews to get started. If you run the `models.py` file, this file gets replaced with an empty database.
- **`queries.py`**: Contains some examples to test back-end logic.
- **`google_client_secrtets.json`**: Authorization information for Google+ authentication. These can be used to try out the authorization options. However, for serious use, you should aquire your own keys.

### Usage:
1. Clone this repository to your desktop, go to the root directory and run:
```python
python models.py
```
Now the database has been created. To run the application type:
```python
python run.py
```
If you want to populate the database with some dummy data type:
```python
python queries.py
```

2. Go to [localhost:5000](http://127.0.0.1:5000/) to see the application running.

### Built With:
- [Flask](http://flask.pocoo.org/): Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
- [SQLAlchemy](https://www.sqlalchemy.org/): SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- [Bootstrap 3](http://getbootstrap.com/): Bootstrap is the most popular HTML, CSS, and JS framework for developing responsive, mobile first projects on the web.
- [JQuery](https://jquery.com/): jQuery is a fast, small, and feature-rich JavaScript library..
- [Jinja2](http://jinja.pocoo.org/docs/2.9/): Jinja2 is a modern and designer-friendly templating language for Python, modelled after Django’s templates.
- [httplib2](https://pypi.python.org/pypi/httplib2/0.9.2): A comprehensive HTTP client library, httplib2 supports many features left out of other HTTP libraries.
- [oauth2client](https://pypi.python.org/pypi/oauth2client): oauth2client is a client library for OAuth 2.0.

### License:
This software is licensed under the [Modified BSD License](https://opensource.org/licenses/BSD-3-Clause).