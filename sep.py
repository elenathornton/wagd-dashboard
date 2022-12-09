import csv
import numpy as np
import pandas as pd
file_name = "Stormy_TrottBaseline"
f=open("input/"+file_name)
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
df.to_csv( "output/" + file_name + ".csv", index = False)



