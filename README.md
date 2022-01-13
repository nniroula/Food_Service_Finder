
### Capstone project 1 API selection

#### API endpoints from yelp fusion api that I will be using in the project are as followings:

1. Base URL:- <br>
     https://api.yelp.com/v3 <br>

2.  Busineses search endpoint <br>
     https://api.yelp.com/v3/businesses/search <br>

3. To get store information based on businesses id parameter<br>

    https://api.yelp.com/v3/businesses/{id} <br>

4. To get local stores based on lacation parameter, categories, limit, and offset<br>

    https://api.yelp.com/v3/businesses/search?location=Denver&categories=restaurants$limit=50&offset=50 

<br>
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

### To simulate the project from scratch:
1. Create a directory, run the commands python3 -m venv venv, source venv/bin/activate, pip install flask

2. To run the server, flask run, or FLASK_APP = my_file.py flask run if your file is named my_file rather than app

3. User jinja templating for template(html file) inheritance, and using templating
4. Update dependencies to requirements.txt file with the command, pip freeze > requirements.txt(this makes requirements.txt)<br>
    Use the command, cat requirements.txt to look up content in requirements.txt file 
