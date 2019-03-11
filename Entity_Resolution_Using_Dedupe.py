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

# Training
if os.path.exists(settings_file):
    with open(settings_file,'rb') as f:
        dedupe = dedupe.StaticDupe(f)
else:
    # Define Dedupe fields
    fields = [
        {'field':'First Name + Last Name','type':'String'},
        {'field':'Location','type':'String'},
        {'field':'Organization','type':'String'},
    ]
    # Dedupe object
    deduper = dedupe.Dedupe(fields)
    # Dedupe train
    deduper.sample(data_d,15000)
    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file, 'rb') as f:
            deduper.readTraining(f)
    # Active Learning
    print('starting active labeling...')

    dedupe.consoleLabel(deduper)

    deduper.train()
    # Write Training to disk
    with open(training_file, 'w') as tf :
        deduper.writeTraining(tf)
    with open(settings_file, 'wb') as sf :
        deduper.writeSettings(sf)

# Threshold score
threshold = deduper.threshold(data_d, recall_weight=2)
# records that match to same entities
print('clustering...')
clustered_dupes = deduper.match(data_d, threshold)

print('# duplicate sets', len(clustered_dupes))
# writing results
cluster_membership = {}
cluster_id = 0
for (cluster_id, cluster) in enumerate(clustered_dupes):
    id_set, scores = cluster
    cluster_d = [data_d[c] for c in id_set]
    canonical_rep = dedupe.canonicalize(cluster_d)
    for record_id, score in zip(id_set, scores) :
        cluster_membership[record_id] = {
            "cluster id" : cluster_id,
            "canonical representation" : canonical_rep,
            "confidence": score
        }

singleton_id = cluster_id + 1

with open(output_file, 'w') as f_output:
    writer = csv.writer(f_output)

    with open(input_file) as f_input :
        reader = csv.reader(f_input)

        heading_row = next(reader)
        heading_row.insert(0, 'confidence_score')
        heading_row.insert(0, 'Cluster ID')
        canonical_keys = canonical_rep.keys()
        for key in canonical_keys:
            heading_row.append('canonical_' + key)

        writer.writerow(heading_row)

        for row in reader:
            row_id = int(row[0])
            if row_id in cluster_membership :
                cluster_id = cluster_membership[row_id]["cluster id"]
                canonical_rep = cluster_membership[row_id]["canonical representation"]
                row.insert(0, cluster_membership[row_id]['confidence'])
                row.insert(0, cluster_id)
                for key in canonical_keys:
                    row.append(canonical_rep[key].encode('utf8'))
            else:
                row.insert(0, None)
                row.insert(0, singleton_id)
                singleton_id += 1
                for key in canonical_keys:
                    row.append(None)
            writer.writerow(row)
