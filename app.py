from flask import Flask

app = Flask(__name__)

@app.route('/')
def base_route():
    return "Started Capstone Project"