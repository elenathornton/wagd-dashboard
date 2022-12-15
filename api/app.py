from io import StringIO
import math
import numpy as np
import pandas as pd
from flask import Flask, request, session, jsonify
import os
import csv
from flask_cors import CORS, cross_origin
import math
from scipy.signal import filtfilt, butter


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

    return jsonify(response_body)


@api.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    print("upload")
    file = request.files['file']
    df = pd.read_csv(file.stream)
    filename = file.filename
    print(filename)
    
    
    
    # measure timestamp
    df['timestamp'] = pd.Series()
    print(df['timestamp'])
    print(df.loc[0, 'timestamp'])
    df.loc[0, 'timestamp'] = 0 # in milliseconds 100 hz = .01 s = 10 milliseconds
    
    for i in range(1, len(df)):
        df.loc[i, 'timestamp'] = (df.loc[i-1, 'timestamp']) + 10
    df['ax'] = (df['ax']*2*9.81)/32768
    df['ay'] = (df['ay']*2*9.81)/32768
    df['az'] = (df['az']*2*9.81)/32768
    df['raw_acceleration'] = df.apply(lambda x: math.sqrt(x['ax']**2 + x['ay']**2 + x['az']**2), axis=1)

    window_size = 10
    mag_data = list(df['raw_acceleration'])
    average_data = np.convolve(mag_data, np.ones(window_size), 'valid') / window_size
    for ind in range(window_size - 1):
        average_data=np.insert(average_data, 0, np.nan)
    df['avg_acceleration'] = average_data



    df['avg_acceleration'] = df['avg_acceleration'].fillna(0)
    threshold = np.percentile(list(df['avg_acceleration']), 60)
    print(threshold)
    avg_data = list(df['avg_acceleration'])
    steps = []
    num_steps = 0
    for i in range(len(avg_data)):
        if i>1:
            if avg_data[i]>threshold and avg_data[i-1]<threshold:
                steps.append(i)
                num_steps+=1
                
                
    radius = 1 
    df['yaw_x'] = radius * np.sin(np.pi * 2 * df['yaw'] / 360)
    df['yaw_y'] = radius * np.cos(np.pi * 2 * df['yaw'] / 360)
    df['pitch_x'] = radius * np.sin(np.pi * 2 * df['pitch'] / 360)
    df['pitch_y'] = radius * np.cos(np.pi * 2 * df['pitch'] / 360)
    df['roll_x'] = radius * np.sin(np.pi * 2 * df['roll'] / 360)
    df['roll_y'] = radius * np.cos(np.pi * 2 * df['roll'] / 360)



    l_ax = list(df['ax'])
    l_ay = list(df['ay'])
    l_az = list(df['az'])
    vx = []
    vy = []
    vz = []
    vx.append(0)
    vy.append(0)
    vz.append(0)
    sx = []
    sy = []
    sz = []
    sx.append(0)
    sy.append(0)
    sz.append(0)
    for i in range(1,len(l_ax)):
        vx.append(vx[i-1]+l_ax[i]*0.01)
        vy.append(vy[i-1]+l_ay[i]*0.01)
        vz.append(vz[i-1]+l_az[i]*0.01)
    for i in range(1,len(l_ax)):
        sx.append(vx[i-1]*0.01 + 0.5*l_ax[i]*0.0001)
        sy.append(vy[i-1]*0.01 + 0.5*l_ay[i]*0.0001)
        sz.append(vz[i-1]*0.01 + 0.5*l_az[i]*0.0001)
    df['vx']=vx
    df['vy']=vy
    df['vz']=vz
    df['sx']=sx
    df['sy']=sy
    df['sz']=sz
    
    response= {"status": 200,
                "duration_ms": df['timestamp'].iat[-1],
                "distance": df['sx'].to_json(),
                "time_ms": df['timestamp'].to_json(),
                "acceleration": df['avg_acceleration'].to_json(),
                "velocity": df['vx'].to_json(),
                "gait metrics": ["TODO"],
                "yaw_x": df['yaw_x'].to_json(),
                "yaw_y": df['yaw_y'].to_json(),
                "pitch_x": df['pitch_x'].to_json(),
                "pitch_y": df['pitch_y'].to_json(),
                "roll_x": df['roll_x'].to_json(),
                "roll_y": df['roll_y'].to_json(),
                "steps": num_steps,
                    
            }
    print(response)
    return jsonify(response)


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
