import json
from csv import reader

basic_txt = 'Visualite/resources/fcm_basic.txt'
one_txt = 'Visualite/resources/fcm_one.txt'

with open(basic_txt, 'r') as file:
    basic_data = json.load(file)

with open(one_txt, 'r') as file:
    one_data = json.load(file)

# Access data like this:
one_cols = data['std_cols']
basic_cols = data['std_cols']
print(std_cols)

file = 'one_sample.csv'
with open(file, 'r') as csv_file:
    csv_reader = reader(csv_file, delimiter=';')

    for i, row in enumerate(csv_reader):
        if i == 3:
            print("cols:")
            print(row)