'''
This script will run keep running in the background and update the DE locations txt
'''

from tempfile import NamedTemporaryFile
import shutil
import csv

filename = 'delivery_executives.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)

fields = ['ID', 'curr_Latitude', 'curr_longitude', 'state', 'final_latitude', 'final_longitude', 'current_Order', 'past_Orders']

with open(filename, 'r') as csvfile, tempfile:
    reader = csv.DictReader(csvfile, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields)
    for row in reader:
        if row['current_Order'] == str('-1'):
            print('updating row', row['ID'])
        row = {'ID': row['ID'], 'Name': row['Name'], 'Course': row['Course'], 'Year': row['Year']}
        writer.writerow(row)

shutil.move(tempfile.name, filename)
