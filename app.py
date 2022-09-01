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


# global variables
# suggested_stores = []
# other_stores_to_explore = []


@app.route('/restaurants')
def show_food_service_providers_from_api():
    """ Take in user input of the city and render all food stores from the external api in the browser based on the user input """

    headers= {"Authorization": f"Bearer {api_key}" }
    city_name = request.args['city']  # not requests, get user input from the browser

    NEEDED_API_URL = f'{BASE_URL}{BUSINESS_ENDPOINT}?location={city_name}&term=Restaurant'

    api_response = requests.get(NEEDED_API_URL, headers= headers)
    api_data = api_response.json() # returns data in json format
    api_stores_object = api_data['businesses']

    #  list to hold stores
    suggested_stores = []
    other_stores_to_explore = []

    suggested_stores_array = []

    for store in api_stores_object:
        suggested_stores_object = {}
  
        if(store['rating'] >= 2.5):
            suggested_stores.append(store['name'])

            # remove this at the end
            store_id = store['id']

            suggested_stores_object['name'] = store['name']
            suggested_stores_object['id'] = store['id']
            suggested_stores_array .append(suggested_stores_object)
    
        else:
            other_stores_to_explore.append(store['name'])
        
    length_of_suggested_stores = len(suggested_stores)
    length_of_other_stores = len(other_stores_to_explore)

    print("*****************************")
    print(f"suggested stores array is {suggested_stores_array}")

    print("*****************************")

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
                            length_of_other_stores = length_of_other_stores,
                            api_stores_object = api_stores_object,
                            # api_retrieved_store = api_retrieved_store,
                            store_id = store_id,

                            suggested_stores_array = suggested_stores_array
                        )


################################################################################

""" Data manupulation routes """
#  Details page

""" GET https://api.yelp.com/v3/businesses/{id} """

@app.route('/restaurant/<restaurant_id>')
def show_details_about_restaurant(restaurant_id):
    """ use the store id to grab data from the api """

    headers= {"Authorization": f"Bearer {api_key}" }
    # city_name = request.args['city']  # not requests, get user input from the browser

    NEEDED_API_URL = f'{BASE_URL}/businesses/{restaurant_id}'

    api_response = requests.get(NEEDED_API_URL, headers= headers)
    store_data = api_response.json() # returns data in json format
    # api_stores_object = api_data['businesses']
    address = store_data['location'][ 'display_address'] # returns an array(list)
    address_to_string = ' '.join(address)

    hours = store_data['hours']
    first_data_in_hours = hours[0]
    list_of_hours_for_seven_days = first_data_in_hours['open']

    monday_hours = list_of_hours_for_seven_days[0]
    opening_time_of_monday = monday_hours['start']
    closing_time_of_monday = monday_hours['end']
    business_hours_of_monday = opening_time_of_monday + ' - ' + closing_time_of_monday

    tuesday_hours = list_of_hours_for_seven_days[1]
    opening_time_of_tuesday = tuesday_hours['start']
    closing_time_of_tuesday = tuesday_hours['end']
    business_hours_of_tuesday = opening_time_of_tuesday + ' - ' + closing_time_of_tuesday

    # wednesday
    wednesday_hours = list_of_hours_for_seven_days[2]
    opening_time_of_wednesday = wednesday_hours['start']
    closing_time_of_wednesday = wednesday_hours['end']
    business_hours_of_wednesday = opening_time_of_wednesday + ' - ' + closing_time_of_wednesday

    # Thursday
    thursday_hours = list_of_hours_for_seven_days[3]
    opening_time_of_thursday = thursday_hours['start']
    closing_time_of_thursday = thursday_hours['end']
    business_hours_of_thursday = opening_time_of_thursday + ' - ' + closing_time_of_thursday

    # Friday
    friday_hours = list_of_hours_for_seven_days[4]
    opening_time_of_friday = friday_hours['start']
    closing_time_of_friday = friday_hours['end']
    business_hours_of_friday = opening_time_of_friday + ' - ' + closing_time_of_friday

    # Saturday
    saturday_hours = list_of_hours_for_seven_days[5]
    opening_time_of_saturday = saturday_hours['start']
    closing_time_of_saturday = saturday_hours['end']
    business_hours_of_saturday = opening_time_of_saturday + ' - ' + closing_time_of_saturday

    # Sunday
    sunday_hours = list_of_hours_for_seven_days[6]
    opening_time_of_sunday = sunday_hours['start']
    closing_time_of_sunday = sunday_hours['end']
    business_hours_of_sunday = opening_time_of_sunday + ' - ' + closing_time_of_sunday


    return render_template('restaurant-details.html', 
                            store_data = store_data,
                            address =  address_to_string,
                            business_hours_of_monday = business_hours_of_monday,
                            business_hours_of_tuesday = business_hours_of_tuesday,
                            business_hours_of_wednesday = business_hours_of_wednesday,
                            business_hours_of_thursday = business_hours_of_thursday,
                            business_hours_of_friday = business_hours_of_friday,
                            business_hours_of_saturday = business_hours_of_saturday,
                            business_hours_of_sunday = business_hours_of_sunday
                        )
    
   


# headers= {"Authorization": f"Bearer {api_key}" }
# # NEEDED_API_URL = f'{BASE_URL}{BUSINESS_ENDPOINT}?location=Denver&term=Restaurant'

# NEEDED_API_URL = 'https://api.yelp.com/v3/businesses/64sM5k1cgyVBwV6YBJ-zWQ'

# api_response = requests.get(NEEDED_API_URL, headers= headers)
# store_data = api_response.json() # returns data in json format
# # data_object = api_data['businesses']

# # for val in data_object:
# #     print('#################################################################')
# #     print(val['name'])
# #     print(val['is_closed'])
# #     print(val['display_phone'])
# #     address = val['location'][ 'display_address'] # returns an array(list)
# #     address_to_string = ' '.join(address)
# #     print(address_to_string)
# #     print(val['rating'])

# store = store_data['hours']
