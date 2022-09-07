from flask import Flask, render_template, request, redirect, flash, session, g
# for debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
import requests
from secret import API_SECRET_KEY


#  sqlalchemy
# from flask_sqlalchemy import SQLAlchemy

# models
from models import FavoriteStores, db, connect_db, User
# form
from forms import AddAUserForm, LoginForm

from flask_bcrypt import Bcrypt

from sqlalchemy.exc import IntegrityError 

bcrypt = Bcrypt()

# current user to track login status
CURRENT_USER_ID = "current_user_id"
USER_ID_IN_ACTION = -1

app = Flask(__name__)  

# # Get DB_URI from environ variable (useful for production/testing) or,
# # if not set there, use development local db.
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql:///restaurants_bd'))

#  To connect to database
# Update the database name before useing it
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurants_db'

#  flask debugtoolbar setup
app.config['SECRET_KEY'] = "nosecretkeyhere"

#  FOR TESTING, comment out debug, Uncomment after testing
debug = DebugToolbarExtension(app)

# ********

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True  # I commented this out
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 

# ***********

# from models
connect_db(app)

######################################################################################################

@app.route('/')
def home():
    return render_template('home-page.html')

# secret route, you cannot access this route without being logged in

@app.route('/search')
def search_restaurants():
    if  "current_user_id" not in session:
        flash("You must be logged in to search for restaurants.")
        return redirect('/')
    else:
        return render_template('/cities/city_form.html')


######################################################################################################

""" User route, signup, login, logout """

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURRENT_USER_ID in session:
        g.user = User.query.get(session[CURRENT_USER_ID])

    else:
        g.user = None


@app.route('/signup', methods=["GET", "POST"])
def signup():

    form = AddAUserForm()

    if form.validate_on_submit():
        try:
            first_name=form.firstname.data
            last_name=form.lastname.data
            user_name=form.username.data
            pass_word=form.password.data

            hashed_pwd = bcrypt.generate_password_hash(pass_word).decode("utf8") 
            user = User.signup(first_name, last_name, user_name, hashed_pwd)

            db.session.add(user)
            db.session.commit()
            flash('Signed up successfully!')
            flash('Please login to verify your credentials')

            return redirect("/login")

        except IntegrityError:
            flash("Username already taken")
            flash("please signup with a different username")
            return render_template('users/signup_form.html', form=form)
  
    return render_template('/users/signup_form.html', form = form)

 
@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit(): 
        user_name = form.username.data
        pass_word = form.password.data

        user = User.authenticate(user_name, pass_word)

        if user:
            session["current_user_id"] = user.id
    
            flash(f"Hello, {user.username}!, you are logged in")
            flash('Enter city and state to search for local restaurant')

            # protected route, cannot see without logging in
            return redirect('/search')
        # flash("Invalid credentials.", 'danger')
        flash("Invalid credentials. Try again.")
        # return render_template('/users/login_form.html')
       
    return render_template('/users/login_form.html', form=form)

@app.route('/logout')
def logout():

    if CURRENT_USER_ID in session:
        session.pop(CURRENT_USER_ID)
    return redirect('/login')


######################################################################################################

""" Geneeal purpose functions """
import random

def generate_random_list_of_items(arrayOfItems):
    """ generates a list of 12 randomly selected items from a list """

    list_of_twelve_random_items = random.sample(arrayOfItems, 12)
    return list_of_twelve_random_items


######################################################################################################
""" External API Access and data retrieval as well as manipulation """

api_key = API_SECRET_KEY
BASE_URL = 'https://api.yelp.com/v3'
BUSINESS_ENDPOINT = '/businesses/search'

RATING = 2.5


@app.route('/restaurants')
def show_food_service_providers_from_api():
    """ Take in user input of the city and render all restaurants from the external api in the browser based on the user input """

    headers= {"Authorization": f"Bearer {api_key}" }
    city_name = request.args['city']  # not requests, get user input from the browser

    NEEDED_API_URL = f'{BASE_URL}{BUSINESS_ENDPOINT}?location={city_name}&term=Restaurant'

    api_response = requests.get(NEEDED_API_URL, headers= headers)
    api_data = api_response.json() # returns data in json format
    api_stores_object = api_data['businesses']

    suggested_stores_array = []
    other_stores_array = []

    for store in api_stores_object:
        suggested_stores_object = {}
        other_stores_object = {}
  
        if(store['rating'] >= RATING):
            suggested_stores_object['name'] = store['name']
            suggested_stores_object['id'] = store['id']
            suggested_stores_array .append(suggested_stores_object)
    
        else:
            other_stores_object['name'] = store['name']
            other_stores_object['id'] = store['id']
            other_stores_array.append(other_stores_object)
        
    length_of_suggested_stores_array = len(suggested_stores_array)
    length_of_other_stores_array = len(other_stores_array)

    if(length_of_suggested_stores_array > 12):
        list_of_randomly_selected_suggested_restaurants = generate_random_list_of_items(suggested_stores_array)
        suggested_stores_array.clear()

        for restaurant in list_of_randomly_selected_suggested_restaurants:
            suggested_stores_array.append(restaurant)
    
    if(length_of_other_stores_array > 12):
        list_of_randomly_selected_other_restaurants = generate_random_list_of_items(other_stores_array)
        other_stores_array.clear()

        for restaurant in list_of_randomly_selected_other_restaurants:
            other_stores_array.append(restaurant)

    return render_template('/stores/food_providers.html', 
                            suggested_stores_array = suggested_stores_array,
                            other_stores_array = other_stores_array,  
                            length_of_suggested_stores_array = length_of_suggested_stores_array,
                            length_of_other_stores = length_of_other_stores_array,
                            api_stores_object = api_stores_object,
                        )

################################################################################

""" Each restaurant's Details route """

@app.route('/restaurant/<restaurant_id>', methods=["POST", "GET"])
def show_details_about_restaurant(restaurant_id):
    """ use the store id to grab data from the api """

    headers= {"Authorization": f"Bearer {api_key}" }
    # """ GET https://api.yelp.com/v3/businesses/{id} """
    NEEDED_API_URL = f'{BASE_URL}/businesses/{restaurant_id}'
    api_response = requests.get(NEEDED_API_URL, headers= headers)
    store_data = api_response.json()
    address = store_data['location'][ 'display_address']
    address_to_string = ' '.join(address)

    keys = store_data.keys()

    if request.method == 'POST':
        stores_in_db = FavoriteStores.query.all()

        # if g.user.id in session:
        if 'current_user_id' in session:
            store_name = store_data['name']
            restaurant_phone = store_data['display_phone']

            favorite_store = FavoriteStores(
                store_name = store_name, 
                user_id = g.user.id,
                store_phone = restaurant_phone,
                store_address = address_to_string
            )

            result = False

            for store in stores_in_db:
                address_userId = favorite_store.store_address != store.store_address and favorite_store.user_id != store.user_id
                phone_userId = favorite_store.store_phone != store.store_phone and favorite_store.user_id != store.user_id
                name_userId = favorite_store.store_name != store.store_name and favorite_store.user_id != store.user_id
         
                if address_userId == True or phone_userId == True or name_userId == True:

                    result = True
                else:
                    result = False

                if result == True:
                    db.session.add(favorite_store)
                    db.session.commit()

            return redirect('/favorites')

    # if request.method == 'GET':
    if 'hours' not in keys:
        hours_unavailable = -1

        return render_template('/stores/restaurant-details.html', 
            store_data = store_data,
            address =  address_to_string,
            hours_unavailable = hours_unavailable
        )
    else:
        hrs = store_data['hours']

        numbered_days = []
        monday_hours = []
        tuesday_hours = []
        wednesday_hours = []
        thursday_hours = []
        friday_hours = []
        saturday_hours = []
        sunday_hours = []
        
        first_data_in_hours = hrs[0] 
        list_of_hours_for_seven_days = first_data_in_hours['open']

        for element in list_of_hours_for_seven_days:
            numbered_days.append(element['day'])
            opening_time = element['start']
            closing_time = element['end']

            if element['day'] == 0:
                business_hours_of_monday = opening_time + ' - ' + closing_time
                monday_hours.append(business_hours_of_monday)
            
            if element['day'] == 1:
                business_hours_of_tuesday = opening_time + ' - ' + closing_time
                tuesday_hours.append(business_hours_of_tuesday)

            if element['day'] == 2:
                business_hours_of_wednesday = opening_time + ' - ' + closing_time
                wednesday_hours.append(business_hours_of_wednesday)

            if element['day'] == 3:
                business_hours_of_thursday = opening_time + ' - ' + closing_time
                thursday_hours.append(business_hours_of_thursday)

            if element['day'] == 4:
                business_hours_of_friday = opening_time + ' - ' + closing_time
                friday_hours.append(business_hours_of_friday)

            if element['day'] == 5:
                business_hours_of_saturday = opening_time + ' - ' + closing_time
                saturday_hours.append(business_hours_of_saturday)

            if element['day'] == 6:
                business_hours_of_sunday = opening_time + ' - ' + closing_time
                sunday_hours.append(business_hours_of_sunday)

        if 0 not in numbered_days:
            monday_hours.append('hours not available')
        if 1 not in numbered_days:
            tuesday_hours.append('hours not available')
        if 2 not in numbered_days:
            wednesday_hours.append('hours not available')
        if 3 not in numbered_days:
            thursday_hours.append('hours not available')
        if 4 not in numbered_days:
            friday_hours.append('hours not available')
        if 5 not in numbered_days:
            saturday_hours.append('hours not available')
        if 6 not in numbered_days:
            sunday_hours.append('hours not available')

    return render_template('/stores/restaurant-details.html', 
                            store_data = store_data,
                            address =  address_to_string,
                            monday_hours = monday_hours,
                            tuesday_hours = tuesday_hours,
                            wednesday_hours = wednesday_hours,
                            thursday_hours = thursday_hours,
                            friday_hours = friday_hours,
                            saturday_hours = saturday_hours,
                            sunday_hours = sunday_hours
                        )

################################################################################

""" Favorite stores route """

@app.route('/favorites')
def favorite_stores():
    """ create a list of user's favorite stores """

    # access database
    user = User.query.get_or_404(g.user.id)

    database_stores = FavoriteStores.query.all()
    
    store_array = []
    for store in database_stores:
        store_object = {}
        if store.user_id == user.id:
            store_object['name'] = store.store_name
            store_object['phone'] = store.store_phone
            store_object['address'] = store.store_address
            store_object['id'] = store.id

            if store_object not in store_array:
                store_array.append(store_object)

    return render_template("/stores/favorite_stores.html", store_array = store_array)


@app.route('/favorite/delete/<int:id>', methods=['POST'])
def delete_favorite_store(id):

    # if 'current_user_id' in session:
    if g.user.id:
        fav_store = FavoriteStores.query.get(id)
    
        db.session.delete(fav_store)
        db.session.commit()

        return redirect('/favorites')

    # display this flash message
    flash("You are not authorized to delete.")

    return redirect('/favorites')

################################################################################
