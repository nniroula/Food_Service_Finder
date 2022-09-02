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

RATING = 2.5

@app.route('/')
def home():
    return render_template('city-form.html')


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

    return render_template('food_providers.html', 
                            suggested_stores_array = suggested_stores_array,
                            other_stores_array = other_stores_array,  
                            length_of_suggested_stores_array = length_of_suggested_stores_array,
                            length_of_other_stores = length_of_other_stores_array,
                            api_stores_object = api_stores_object,
                        )


################################################################################

""" Each restaurant's Details route """

@app.route('/restaurant/<restaurant_id>')
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

    if 'hours' not in keys:
        hours_unavailable = -1

        return render_template('restaurant-details.html', 
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
        
        first_data_in_hours = hrs[0] # a
        list_of_hours_for_seven_days = first_data_in_hours['open'] #b

        for element in list_of_hours_for_seven_days:
            numbered_days.append(element['day'])
            opening_time = element['start']
            closing_time = element['end']

            # monday
            if element['day'] == 0:
                business_hours_of_monday = opening_time + ' - ' + closing_time
                monday_hours.append(business_hours_of_monday)
            
            # tuesday
            if element['day'] == 1:
                business_hours_of_tuesday = opening_time + ' - ' + closing_time
                tuesday_hours.append(business_hours_of_tuesday)

            # wednesday
            if element['day'] == 2:
                business_hours_of_wednesday = opening_time + ' - ' + closing_time
                wednesday_hours.append(business_hours_of_wednesday)

            # thursday
            if element['day'] == 3:
                business_hours_of_thursday = opening_time + ' - ' + closing_time
                thursday_hours.append(business_hours_of_thursday)

            # friday
            if element['day'] == 4:
                business_hours_of_friday = opening_time + ' - ' + closing_time
                friday_hours.append(business_hours_of_friday)

            # saturday
            if element['day'] == 5:
                business_hours_of_saturday = opening_time + ' - ' + closing_time
                saturday_hours.append(business_hours_of_saturday)

            # sunday
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

    return render_template('restaurant-details.html', 
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
