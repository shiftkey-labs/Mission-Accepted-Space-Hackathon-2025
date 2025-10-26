# log into timberlea

# python -m pip install flask
# in project, chmod +x .venv/Scripts/activate
# source .venv/Scripts/activate
#to run app, go to project directory 
#run python -m pip install flask flask-cors
# python -m pip install requests
# python -m pip install pandas
#run python app.py

#then run flask run --host=0.0.0.0 --port=5000

# run flask, flask --app app run
#try screen -S flaskapp python app.py to



from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS
from calculations import *

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return 'SupBro! This is the Flask server running.'

@app.route("/runFunction", methods=["POST", "GET"])
def run_function():
    coordinateList = getCoordinates()
    return jsonify(coordinateList)


@app.route("/isWater/<lat>/<lon>")
def isWater(lat, lon):
    url = f"https://is-on-water.balbona.me/api/v1/get/{lat}/{lon}"
    try:
        response = requests.get(url)
        # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()  
        data = response.json()
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'Other error occurred: {err}'}), 500
    
    return jsonify(data['isWater'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)