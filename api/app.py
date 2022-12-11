import numpy as np
import pandas as pd
from flask import Flask, request, session
import os
import csv
from flask_cors import CORS, cross_origin


api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'


@api.route('/')
@cross_origin()
def start():
    response_body = {
        "Status": "Server is live."
    }

    return response_body


@api.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join('/','raw_data')
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


def parse(file_name):
    print("parse")
    print(file_name
          )
    f=open("raw_data/"+file_name)
    # skip = 3
    new_row = []
    for row in csv.reader(f):
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

    # print(len(new_row))
    num_row = np.array(new_row)
    num_row = num_row.reshape(int(len(new_row)/9),9)
    # print(num_row)
    df = pd.DataFrame(num_row, columns =['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'yaw', 'pitch', 'roll'])
    df.to_csv( "clean_data/" + file_name + ".csv", index = False)