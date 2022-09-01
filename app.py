from flask import Flask, render_template, request   #, redirect
# for debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
import requests
from secret import API_SECRET_KEY


app = Flask(__name__)  

#  flask debugtoolbar setup
app.config['SECRET_KEY'] = "nosecretkeyhere"
debug = DebugToolbarExtension(app)

@app.route('/first')
def base_route():
    # return "Started Capstone Project"
    return render_template('base.html')

# @app.route('/signup')
# def signup():
#     return render_template('landing_page.html')

@app.route('/landing')
def landing_page():
    return render_template('landing_page.html')

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

@app.route('/')
def home():
    return render_template('city-form.html')


@app.route('/city')
def show_food_service_providers_from_api():
    """ Take in user input of the city and render all food stores from the external api in the browser based on the user input """

    headers= {"Authorization": f"Bearer {api_key}" }
    city_name = request.args['city']  # not requests, get user input from the browser

    NEEDED_API_URL = f'{BASE_URL}{BUSINESS_ENDPOINT}?location={city_name}&term=Restaurant'

    api_response = requests.get(NEEDED_API_URL, headers= headers)
    api_data = api_response.json() # returns data in json format
    api_store_lists_object = api_data['businesses']

    #  list to hold stores
    suggested_stores = []
    other_stores_to_explore = []

    for store in api_store_lists_object:
        if(store['rating'] >= 2.5):
            suggested_stores.append(store['name'])
        else:
            other_stores_to_explore.append(store['name'])
        
    length_of_suggested_stores = len(suggested_stores)
    length_of_other_stores = len(other_stores_to_explore)

    # use random geneator function, generate 12 random restaurants
    if(length_of_suggested_stores > 12):
        list_of_randomly_selected_suggested_restaurants = generate_random_list_of_items(suggested_stores)
        #  empty the suggested stores array, and append new values to it
        suggested_stores.clear()
        for restaurant in list_of_randomly_selected_suggested_restaurants:
            suggested_stores.append(restaurant)
    
    if(length_of_other_stores >12):
        list_of_randomly_selected_other_restaurants = generate_random_list_of_items(other_stores_to_explore)
         #  empty the other stores array, and append new values to it
        other_stores_to_explore.clear()
        for restaurant in list_of_randomly_selected_other_restaurants:
            other_stores_to_explore.append(restaurant)

    return render_template('food_providers.html', 
                            suggested_stores = suggested_stores, 
                            other_stores = other_stores_to_explore,  
                            length_of_suggested_stores =  length_of_suggested_stores,
                            length_of_other_stores = length_of_other_stores
                        )


################################################################################


# headers= {"Authorization": f"Bearer {api_key}" }
# NEEDED_API_URL = f'{BASE_URL}{BUSINESS_ENDPOINT}?location=Denver&term=Restaurant'

# api_response = requests.get(NEEDED_API_URL, headers= headers)
# api_data = api_response.json() # returns data in json format
# data_object = api_data['businesses']

# for val in data_object:
#     print('#################################################################')
#     print(val['name'])
#     print(val['is_closed'])
#     print(val['display_phone'])
#     address = val['location'][ 'display_address'] # returns an array(list)
#     address_to_string = ' '.join(address)
#     print(address_to_string)
#     print(val['rating'])
