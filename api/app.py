from io import StringIO
import math
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
    print("upload")
    file = request.files['file']
    file_data = pd.read_csv(file.stream)
    filename = file.filename
    print(filename)
    
    
    
    # measure timestamp
    file_data['timestamp'] = pd.Series()
    print(file_data['timestamp'])
    print(file_data.loc[0, 'timestamp'])
    file_data.loc[0, 'timestamp'] = 0 # in milliseconds 100 hz = .01 s = 10 milliseconds
    
    for i in range(1, len(file_data)):
        file_data.loc[i, 'timestamp'] = (file_data.loc[i-1, 'timestamp']) + 10

    file_data['raw_acceleration'] = file_data.apply(lambda x: math.sqrt(x['ax']**2 + x['ay']**2 + x['az']**2), axis=1)

    print(file_data)
    response= {"status": 200,
                "duration_ms": file_data['timestamp'].iat[-1],
                "distance": 10,
                "time_ms": file_data['timestamp'].array,
                "acceleration": file_data['raw_acceleration'].array,
                "velocity": [],
                "gait metrics": []
            }
    print(response)
    return response


# def parse(file_name):
#     # f=open("raw_data/"+file_name)
#     # skip = 3
#     new_row = []
#     for row in csv.reader(file_name):
#         for i, elem in enumerate(row):
#             print(elem)
#             elem = elem.replace(" ","")
#             if elem == '':
#                 pass
#             if i!=0 and i%8==0 and i!=len(row)-1:
#                 if elem.count('-') == 2:
#                     split_number = elem.split("-")
#                     new_row.append(-1*int(split_number[1]))
#                     new_row.append(-1*int(split_number[2]))
#                 elif elem.count('-') == 1:
#                     if elem[0]=="-":
#                         # print(elem)
#                         new_row.append(int(elem[:4]))
#                         new_row.append(int(elem[4:]))
#                     else:
#                         split_number = elem.split("-")
#                         # print(elem)
#                         new_row.append(int(split_number[0]))
#                         new_row.append(-1 * int(split_number[1]))
#                 elif elem.count('-') == 0:
#                     new_row.append(int(elem[:3]))
#                     new_row.append(int(elem[3:]))
#             else:
#                 new_row.append(int(elem))
#     # print(len(new_row))
#     num_row = np.array(new_row)
#     num_row = num_row.reshape(int(len(new_row)/9),9)
#     # print(num_row)
#     df = pd.DataFrame(num_row, columns =['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'yaw', 'pitch', 'roll'])
#     df.to_csv( "clean_data/" + file_name + ".csv", index = False)
    
    
    
if __name__ == "__main__":
    api.run(host='0.0.0.0', port=8080, debug = True)
