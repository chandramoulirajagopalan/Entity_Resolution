from future.builtins import next
import dedupe
import os
import csv
import re
import collections
import logging
import optparse
from numpy import nan
from unidecode import unidecode

input_file = 'csv_input.csv'
training_file = 'threaded-output.json'
output_file = 'csv_output.csv'
def preProcess(column):
    import unidecode
    column = column.decode("utf8")
    column = unidecode.unidecode(column)
    column = re.sub(' +',' ',column)
    column = re.sub('\n',' ',column)
    column = column.strip().strip('"').strip("'").lower().strip()
    

def readFile(filename):
    """Read CSV file as an input which creates unique ID for each data column"""
    data_Dict = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = [((k,preProcess(v)) for (k,v) in row.items())]
            row_id = int(row['Id'])
            data_d[row_id] = dict(clean_row)
    
    return data_d

print("Importing Data ...")
data_d = readFile(input_file)

if os.path.exists(settings_file):
    with open(settings_file,'rb') as f:
        dedupe = dedupe.StaticDupe(f)
else:
    fields = [
        {'field':'First Name + Last Name','type':'String'},
        {'field':'Location','type':'String'},
        {'field':'Organization','type':'String'},
    ]
    deduper = dedupe.Dedupe(fields)
    deduper.sample(data_d,15000)
    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file, 'rb') as f:
            deduper.readTraining(f)
            
    print('starting active labeling...')

    dedupe.consoleLabel(deduper)

    deduper.train()

    with open(training_file, 'w') as tf :
        deduper.writeTraining(tf)

    with open(settings_file, 'wb') as sf :
        deduper.writeSettings(sf)

print('blocking...')


threshold = deduper.threshold(data_d, recall_weight=2)

print('clustering...')
clustered_dupes = deduper.match(data_d, threshold)

print('# duplicate sets', len(clustered_dupes))
