from flask import Flask

api = Flask(__name__)

@api.route('/')
def start():
    response_body = {
        "name": "Test",
        "about" :"This is a test"
    }

    return response_body