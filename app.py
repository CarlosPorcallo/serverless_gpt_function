
import sys
import openai
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

api_key = os.getenv("API_KEY")


app = Flask(__name__)

#curl -X POST -H "Content-Type: application/json" -d '{"message": [{"role": "user", "content": "Hello!"}]}' http://localhost:5000/message
def completion(my_messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=my_messages
        )    


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.route('/message', methods=['POST'])
def get_message():
    data = request.get_json()  # Obtener datos del cuerpo de la solicitud POST
    print(data)
    if(data["key"]==api_key):
        message = data['message']  # Obtener el valor del parámetro 'message'
        response = completion(message)
        return {'message': response}  # Devolver el mismo mensaje en formato JSON
    else:
        return {'message': "acceso denegado"}


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
