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
    print("upload`")
    file = request.files['file']
    print(request.data)
    print(file)
    file_data = pd.read_csv(file.stream)
    # print(file_data)
    print(file_data)
    filename = file.filename
    
    file_data['raw_acceleration'] = file_data.apply(lambda x: math.sqrt(x.ax**2 + x.ay**2 + x.az**2))

    print(file_data)
    response= {"status": 200,
                "duration": 10.3,
                "distance": 10,
                "acceleration": [],
                "velocity": [],
                "gait metrics": []
            }
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
