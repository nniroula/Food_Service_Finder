from flask import Flask, render_template, request, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests
from secret import API_SECRET_KEY
from models import FavoriteStores, db, connect_db, User
from forms import AddAUserForm, LoginForm, UpdateUserProfileForm
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError 
import random, os

bcrypt = Bcrypt()

CURRENT_USER_ID = "current_user_id"
USER_ID_IN_ACTION = -1

app = Flask(__name__)  

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///restaurants_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "itsasecrettoalldevs")

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

api_key = os.environ.get('API_SECRET_KEY')
BASE_URL = 'https://api.yelp.com/v3'
BUSINESS_ENDPOINT = '/businesses/search'
RATING = 2.5


def generate_random_list_of_items(arrayOfItems):
    """ generates a list of 12 randomly selected items from a list """

    if len(arrayOfItems) < 12:
        list_of_random_items = random.sample(arrayOfItems, len(arrayOfItems))
    else:
        list_of_random_items  = random.sample(arrayOfItems, 12)

    return  list_of_random_items 


def alphabetic_name(name):
    """ Returns True if all the characters in a user input are alphabets. """

    alphabet_only_name = name.isalpha()
    return alphabet_only_name 

def alphanumeric_username(username):
    """ Returns True if the characters in username are either alphabet, numbers, or both. """

    only_alphanumeric_username = username.isalnum()
    return only_alphanumeric_username 


@app.route('/')
def home():
    """ renders the base url of the local restaurants finder web app."""

    return render_template('home-page.html')


@app.route('/search')
def search_restaurants():
    """ secret route, you cannot access this route without being logged in. """

    if  "current_user_id" not in session:
        flash("You must be logged in to search for restaurants.")
        return redirect('/')
    else:
        return render_template('/cities/city_form.html')


@app.before_request
def add_user_to_g():
    """Add current logged in user to Flask global."""

    if CURRENT_USER_ID in session:
        g.user = User.query.get(session[CURRENT_USER_ID])

    else:
        g.user = None


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ Create a user account. """

    form = AddAUserForm()
    valid_input = True

    if form.validate_on_submit():
        try:
            first_name=form.firstname.data
            last_name=form.lastname.data
            user_name=form.username.data
            pass_word=form.password.data

            existing_user = User.query.filter_by(username = user_name).first()
            not_existing_user = existing_user == None

            if alphabetic_name(first_name) == False:
                first_name_error = "First name should contain only letters."
                valid_input = False
            else:
                first_name_error = ''
            
            if alphabetic_name(last_name) == False:
                last_name_error = "Last name should contain only letters."
                valid_input = False
            else:
                last_name_error = ''

            if alphanumeric_username(user_name) == False:
                user_name_error = "Username should contain only letters and numbers."
                valid_input = False
            else:
                user_name_error = ''

            if not_existing_user == False:
                user_name_error = "Username is taken. Sign up with a different one."
                valid_input = False
          
            if valid_input == False:
                return render_template('/users/signup_form.html', form = form, first_name_error = first_name_error,
                     last_name_error = last_name_error, user_name_error = user_name_error)

            else:
                if not_existing_user == True:
                    user = User.signup(first_name, last_name, user_name, pass_word)

                    db.session.add(user)
                    db.session.commit()

                    flash('Signed up successfully!')
                    return redirect("/login")

        except IntegrityError:
            return render_template('users/signup_form.html', form=form)
  
    return render_template('/users/signup_form.html', form = form)

 
@app.route('/login', methods=["GET", "POST"])
def login():
    """ Allows a user to login. Checks if the user is not yet signed up, and also if password and username are valid."""

    form = LoginForm()

    if form.validate_on_submit(): 
        user_name = form.username.data
        pass_word = form.password.data

        try:
            user = User.authenticate(user_name, pass_word)
        except:
            invalid_user = "User does not exist! Enter a valid username."
            return render_template('/users/login_form.html', form = form, invalid_user = invalid_user)
        else:
            if user:
                session["current_user_id"] = user.id
                flash(f"Hello, {user.username}!, you are logged in.")
                return redirect('/search')
            invalid_password = "Invalid password! Please try again."
            return render_template('/users/login_form.html', form = form, invalid_password = invalid_password)
       
    return render_template('/users/login_form.html', form=form)


@app.route('/logout')
def logout():
    """ logs out a currently logged in user."""

    if CURRENT_USER_ID in session:
        session.pop(CURRENT_USER_ID)
    return redirect('/login')


@app.route('/restaurants')
def show_food_service_providers_from_api():
    """ Take in user input of the city and render all restaurants from the external api in the browser based on the user input """

    headers= {"Authorization": f"Bearer {api_key}" }
    try:
        city_name = request.args['city']
        NEEDED_API_URL = f'{BASE_URL}{BUSINESS_ENDPOINT}?location={city_name}&term=Restaurant'
        api_response = requests.get(NEEDED_API_URL, headers= headers)
        api_data = api_response.json()
        api_stores_object = api_data['businesses']
    except KeyError:
        flash('Invalid input! Please try again.')
        return render_template('/cities/city_form.html')
    else:
        suggested_stores_array, other_stores_array = [], []

        for store in api_stores_object:
            suggested_stores_object, other_stores_object = {}, {}
    
            if store['rating'] >= RATING:
                suggested_stores_object['name'] = store['name']
                suggested_stores_object['id'] = store['id']
                suggested_stores_array .append(suggested_stores_object)
            else:
                other_stores_object['name'] = store['name']
                other_stores_object['id'] = store['id']
                other_stores_array.append(other_stores_object)
            
        length_of_suggested_stores_array = len(suggested_stores_array)
        length_of_other_stores_array = len(other_stores_array)

        if length_of_suggested_stores_array > 12:
            list_of_randomly_selected_suggested_restaurants = generate_random_list_of_items(suggested_stores_array)
            suggested_stores_array.clear()

            for restaurant in list_of_randomly_selected_suggested_restaurants:
                suggested_stores_array.append(restaurant)
        
        if length_of_other_stores_array > 12:
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


@app.route('/restaurant/<restaurant_id>', methods=["POST", "GET"])
def show_details_about_restaurant(restaurant_id):
    """ Provides details about a restaurant. Uses the store id to grab data from the api. """

    headers= {"Authorization": f"Bearer {api_key}" }
    NEEDED_API_URL = f'{BASE_URL}/businesses/{restaurant_id}'
    api_response = requests.get(NEEDED_API_URL, headers= headers)
    store_data = api_response.json()
    address = store_data['location'][ 'display_address']
    address_to_string = ' '.join(address)

    keys = store_data.keys()

    if request.method == 'POST':
        fav_stores_in_db = FavoriteStores.query.all()

        if 'current_user_id' in session:
            store_name = store_data['name']
            restaurant_phone = store_data['display_phone']

            favorite_store = FavoriteStores(store_name = store_name, user_id = g.user.id, store_phone = restaurant_phone,
                store_address = address_to_string)

            if len(fav_stores_in_db) == 0:
                db.session.add(favorite_store)
                db.session.commit()
                return redirect('/favorites')
            else:
                result = False

                for store in fav_stores_in_db:
                    address_userId = favorite_store.store_address != store.store_address 
                    phone_userId = favorite_store.store_phone != store.store_phone 
                    name_userId = favorite_store.store_name != store.store_name 
            
                    if address_userId == True or phone_userId == True or name_userId == True:
                        result = True
                    else:
                        result = False

                if result == True:
                    db.session.add(favorite_store)
                    db.session.commit()
                    return redirect('/favorites')
                else:
                    flash('The store is already in your favorite list!')

    # if request.method == 'GET':
    if 'hours' not in keys:
        hours_unavailable = -1

        return render_template('/stores/restaurant-details.html', store_data = store_data, address = address_to_string,
            hours_unavailable = hours_unavailable)
    else:
        hrs = store_data['hours']

        numbered_days, monday_hours, tuesday_hours, wednesday_hours = [], [], [], []
        thursday_hours, friday_hours, saturday_hours, sunday_hours = [], [], [], []
    
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


@app.route('/favorites')
def favorite_stores():
    """ Creates a list of user's favorite restaurants. """

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

    if g.user.id:
        fav_store = FavoriteStores.query.get(id)
        db.session.delete(fav_store)
        db.session.commit()
        return redirect('/favorites')

    flash("You are not authorized to delete.")
    return redirect('/favorites')


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """ Updates user profile for current user. Avoid passing/updating password here. """

    if 'current_user_id' not in session:
        return redirect('/')

    user = User.query.get_or_404(g.user.id)           
    form = UpdateUserProfileForm(obj = user)   

    if form.validate_on_submit():
        user_to_be_updated = True

        if User.authenticate(user.username, form.password.data):
            try: 
                if alphabetic_name(form.firstname.data) == False:
                    error_in_firstname = "Invalid first name! It contains only letters."
                    user_to_be_updated = False
                else:
                    user.firstname = form.firstname.data
                    error_in_firstname = ''

                if alphabetic_name(form.lastname.data) == False:
                    error_in_lastname = "Invalid last name! It contains only letters."
                    user_to_be_updated = False
                else:
                    user.lastname = form.lastname.data
                    error_in_lastname = ''

                if alphanumeric_username(form.username.data) == False:
                    error_in_username = "Invalid username! It contains only letters and numbers."
                    user_to_be_updated = False
                else:
                    user.username = form.username.data
                    error_in_username = ''
                
                if user_to_be_updated == False:
                    return render_template('/users/profile_page.html', form = form, user = user,
                     error_in_firstname = error_in_firstname, error_in_lastname = error_in_lastname, 
                      error_in_username = error_in_username) 
                else:
                    db.session.commit()  
                    flash("Profile updated successfully!", "primary") 
                    return redirect('/search')
            except IntegrityError:
                error_in_username = 'Username you are about to update is already taken!'
                return render_template('/users/profile_page.html', form = form, user = user, error_in_username = error_in_username) 
        else:
            error_in_password = "Invalid password! You are unauthorized to update the profile."
        return render_template('/users/profile_page.html', form = form, user = user, error_in_password = error_in_password) 
    else:
        return render_template('/users/profile_page.html', form = form, user = user)


@app.errorhandler(404)
def page_not_found(e):
    """ Add page not found error message. set the 404 status explicitly. """

    return render_template('four_O_four_page.html'), 404
