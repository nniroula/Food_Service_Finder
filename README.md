
# Local Restaurants Finder web app

### Description
This app can be used to find local restaurants based on the city and state. It is build using the yelp Fusion API. It recommends a list of tweleve random restaurants at maximum at a time. If there are any other restaurants other than those meeting the recommendation criteria, then those restaurants will be displayed under the heading "other restaurants to explore".

<br>

### User interfacing
- The first time user has to sign up for an account. Once signed up, you will be directed to the login page where you have to login to verify your credentials. The recurring user can click on login button to login to the site. 
- Once logged in, you will have the option to search for the local restaurants. 
- Providing the city and state name would serve best for you to search for the local restaurants.
- Clicking on the restaurant name would render the details about that restaurant. The details include the restaurant name, phone number, address, and hours of operation. The datails page gives a user the option to like that restaurant. If clicked on the star to like the restaurant, a user will be redirected to the favorite stores list page. Here, a user will be able to see the stores that are liked. This page provides an option(or star) to dislike the store if a logged in user wishes to do so. If disliked a store, a user will still be on the same page. The navbar gives different options to either search for other stores, go to the home page, or logout. 
- The store in a favorite store list shows only the name, phone number, and the address.
- The profile icon gives an option for the logged in user to update the profile information.

<br>


### Tech Stack
Flask, Python, Flask_SQLAlchemy, Flask_wtf (Flask What The Form), Psycopg-2, PostgreSQL, Jinja2 templates, HTML5, CSS, Bootstrap

<br>

### API endpoints from yelp fusion api that are used in the project are as followings:

1. Base URL:- <br>
    https://api.yelp.com/v3 <br>

2.  Busineses search endpoint <br>
    https://api.yelp.com/v3/businesses/search <br>

3. To get store information based on businesses id parameter<br>
    https://api.yelp.com/v3/businesses/{id} <br>

4. To get local stores based on the lacation parameter, and the category <br>
    Base URL/Busineses search endpoint?location=cityName&term=Restaurant

<br>

### Relational tables:

users&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; favorite_stores <br>
---------------------------------------------------------------------------
id [PK]&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id [PK]<br>
first_name &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name_of_store <br>
last_name   &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user_id [FK]<br>
password &nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <br>
phone number&nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  <br>
image_url &nbsp;&nbsp; &nbsp;
<br>
<br>

## To simulate the project from scratch:
### A. Initial setup
1. Create a directory, run the commands python3.10 -m venv venv, source venv/bin/activate, pip install flask. (If you wish to download the source code and use it, do ```pip install ir requirements.txt```.)

2. To run the server, ```flask run```, or ```FLASK_APP = my_file.py flask run``` if your file is named my_file rather than app

3. Use jinja templating for templates(html files)
4. Update dependencies to requirements.txt file with the command, ```pip freeze > requirements.txt```. (To make requirements.txt file run the command ```touch requirements.txt``` and to look up content in requirements.txt file - run the command ```cat requirements.txt```)<br>
  
### B. Testing
#### To run test files, use the following - 
1. FOR TESTING, comment out debug in app.py file, Uncomment after testing (comment debug = DebugToolbarExtension(app))
2. cd into your project's virtual environment directory(venv folder)
3. Run the commands: 
```python -m unittest test_file_name``` OR ```FLASK_ENV=production python -m unittest test_file_name```
For example :- ```python -m unittest test_app_routes.py```

### C. Running seed file
If you want to seed the database with some preexisting data, use the following
1.  cd into to your project virtual environment directory(venv folder), and run the commands: 
2. ```createdb your database name```. For example ```createdb restaurants_db```. This must be the databse used in your project.
3.  ```python your_seed_file_name```. For example ```python seed.py``` 

### D. Running Database in terminal
If you want to simultaneously check what is being added/updated in your database, you can do the following
1.  ```psql```
2.  ```\c name of your database```. For Example: \c restaurants_db
3.  ```\dt+``` to check for the relational tables
4.  ```select * from table_name```. For example ```select * from users``` or ``` select * from someother table name``` to check what the table contains

### E. Deployment
This is project is deployed to the Heroku with the following link:
https://local-restaurants-finder.herokuapp.com/ 





 