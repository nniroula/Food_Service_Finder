from flask import Flask, render_template  #, redirect, request 
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
BUSINESS_ENDPOINT = 'businesses/search'
# NEED_API_URL =  'https://api.yelp.com/v3/businesses/search'



# working version
API_URL =  'https://api.yelp.com/v3/businesses/search?location=Denver' #hard coded location
# Working version
headers= {"Authorization": f"Bearer {api_key}" }

#  working version
api_response = requests.get(API_URL, headers= headers)

api_data = api_response.json() # returns data in json format

data_object = api_data['businesses']
# print(data_object[0])


for val in data_object:
    print('#################################################################')
    print(val['name'])
    print(val['is_closed'])
    print(val['display_phone'])
    address = val['location'][ 'display_address'] # returns an array(list)
    address_to_string = ' '.join(address)
    print(address_to_string)
   
