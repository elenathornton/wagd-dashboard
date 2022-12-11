from io import StringIO
import numpy as np
import pandas as pd
from flask import Flask, request, session
import os
import csv
from flask_cors import CORS, cross_origin



api = Flask(__name__)
api.debug = True
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
api.secret_key = 'super secret key'
api.config['SESSION_TYPE'] = 'filesystem'


@api.route('/')
@cross_origin()
def start():
    response_body = {
        "Status": "Server is live."
    }

    return response_body


@api.route('/upload', methods=['POST'])
def fileUpload():
    print("upload`")
    file = request.files['file']
    print(request.data)
    print(file)
    file_data = file.read().decode("utf-8")
    print(file_data)
    parse(file_data)
    filename = file.filename
    print(filename)
    # destination="/".join(['/home/ec2-user/wagd-dashboard/api/raw_data', filename])
    # print(destination)
    # file.save(destination)
    # session['uploadFilePath']=destination
    response="success"
    return response


def parse(file_name):
    print("parse")
    # f=open("raw_data/"+file_name)
    # skip = 3
    new_row = []
    for row in csv.reader(file_name):
        for i, elem in enumerate(row):
            elem = elem.replace(" ","")
            if i!=0 and i%8==0 and i!=len(row)-1:
                if elem.count('-') == 2:
                    split_number = elem.split("-")
                    new_row.append(-1*int(split_number[1]))
                    new_row.append(-1*int(split_number[2]))
                elif elem.count('-') == 1:
                    if elem[0]=="-":
                        # print(elem)
                        new_row.append(int(elem[:4]))
                        new_row.append(int(elem[4:]))
                    else:
                        split_number = elem.split("-")
                        # print(elem)
                        new_row.append(int(split_number[0]))
                        new_row.append(-1 * int(split_number[1]))
                elif elem.count('-') == 0:
                    new_row.append(int(elem[:3]))
                    new_row.append(int(elem[3:]))
            else:
                new_row.append(int(elem))

    print("trying")
    # print(len(new_row))
    num_row = np.array(new_row)
    num_row = num_row.reshape(int(len(new_row)/9),9)
    # print(num_row)
    df = pd.DataFrame(num_row, columns =['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'yaw', 'pitch', 'roll'])
    df.to_csv( "clean_data/" + file_name + ".csv", index = False)
    
    
    
if __name__ == "__main__":
    api.run(host='0.0.0.0', port=8080, debug = True)
