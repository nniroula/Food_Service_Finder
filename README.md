
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