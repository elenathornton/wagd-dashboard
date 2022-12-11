from flask import Flask, request, session
import os

api = Flask(__name__)

@api.route('/')
def start():
    response_body = {
        "Status": "Server is live."
    }

    return response_body


@api.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join('/','test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    print("upload`")
    file = request.files['file']
    filename = file.filename
    print(filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response="success"
    return response