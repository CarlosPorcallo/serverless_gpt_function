import sys
import openai
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
api_key = os.getenv("API_KEY")
app = Flask(__name__)

# Methods
def completion(my_message):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "assistant",
            "content": my_message
        }]
    )

def get_img(my_prompt):
    request = openai.Image.create(
        prompt=my_prompt,
        n=1,
        size="256x256"
    )
    return request["data"][0]["url"]

# API Endpoints
@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')

@app.route('/message', methods=['POST'])
def get_message():
    data = request.get_json()  # Obtener datos del cuerpo de la solicitud POST
    if(data["key"] == api_key):
        message = data['message']  # Obtener el valor del parámetro 'message'
        response = completion(message)
        return {
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': os.getenv("ALLOWED_ORIGINS"),
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'message': response
        }  # Devolver el mismo mensaje en formato JSON
    else:
        return {'message': "Acceso Denegado"}
    
@app.route('/image', methods=['POST'])
def get_image():
    data = request.get_json()  # Obtener datos del cuerpo de la solicitud POST
    if(data["key"] == api_key):
        message = data['message']  # Obtener el valor del parámetro 'message'
        response = get_img(message)
        return {
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': os.getenv("ALLOWED_ORIGINS"),
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'message': response
        }  # Devolver el mismo mensaje en formato JSON
    else:
        return {'message': "Acceso Denegado"}

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)