import os
import csv

from functions import setClosestTime
from functions import convertTimetoDistance
from functions import calculateClosestAngle
from functions import calculateFurthestAngle
from functions import calculateDepth
from functions import calculatePosition
from functions import determineRange
from functions import comparePositionloop
from functions import displayResults

v_sound = 0.154 #cm/us change depending on speed found
L = 2.5 #cm
rightangle = 1.571 #angles in radians
data_list = []
timer = 0

with open ('experiments.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count=0
    list_x = []
    for row in csv_reader:
        while True:
            try:
                input_t1 = float(row['Average1'])
                input_t2 = float(row['Average2'])
        
                t1,t2 = setClosestTime(input_t1,input_t2)
                d1,d2 = convertTimetoDistance(t1,t2)
                a1 = calculateClosestAngle(d1,d2,L)
                a2 = calculateFurthestAngle(d1,d2,L)
                d = calculateDepth(a1,a2,L)
                x_values = calculatePosition(a2,d2)
                position = determineRange(x_values,a1,L)
                list_x.append(x_values)
                #print(list_x)
                timer,comparison = comparePositionloop(timer,list_x)
                displayResults(position,comparison)
                break
            except ValueError: #math error but still stores previous x in list 
                print(f"Data number {len(list_x)+1} is invalid.")
                position = "Invalid triangle"
                comparison = "Invalid triangle"
                list_x.append(x_values)
                timer += 1
                break

       
        data_dict = {"Index": timer,"T1": t1,"T2": t2, "D1": d1, "D2": d2, "A1": a1, "A2": a2, "D": d, "X": x_values,"Position": position, "Comparison": comparison}
        data_list.append(data_dict)

csv_file.close()

#print(data_list)


with open('experiments_processed.csv', mode='w') as csv_file:
    fieldnames = ['Index','T1','T2','D1','D2','A1','A2','D','X','Position','Comparison']
    writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    
    writer.writeheader()
    for data_row in data_list:
        writer.writerow(data_row)
        
csv_file.close()

