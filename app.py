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
""" External API """
api_key = API_SECRET_KEY

BASE_URL = 'https://api.yelp.com/v3'
BUSINESS_ENDPOINT = '/businesses/search'

@app.route('/')
def home():
    return render_template('city-form.html')


@app.route('/city')
def show_all_food_service_providers_from_api():
    """ Take in user input of the city and render all food stores from the external api in the browser based on the user input """

    headers= {"Authorization": f"Bearer {api_key}" }
    city_name = request.args['city']  # not requests, get user input from the browser

    # API_URL =  f'https://api.yelp.com/v3/businesses/search?location={city_name}'
    NEEDED_API_URL =  f'{BASE_URL}{BUSINESS_ENDPOINT}?location={city_name}'

    api_response = requests.get(NEEDED_API_URL, headers= headers)
    api_data = api_response.json() # returns data in json format
    data_object = api_data['businesses']

    for val in data_object:
        print('#################################################################')
        print(val['name'])
        print(val['is_closed'])
        print(val['display_phone'])
        address = val['location'][ 'display_address'] # returns an array(list)
        address_to_string = ' '.join(address)
        print(address_to_string)
        print(val['rating'])

    return render_template('food_providers.html', data_object = data_object)


################################################################################


   
