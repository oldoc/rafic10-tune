import csv
from numpy import array

data = []

with open('input.csv','r', newline='') as file:
    file = csv.reader(file, delimiter=',')
    for row_list in file:
        row_list_int = [value for value in row_list]
        data.append(row_list_int)
data = array(data)

print(data[0][1])