import argparse
import os
import json
import csv

parser = argparser.ArgumentParser()
parser.add_argument('-n','--first-last', help = "First Name and Last Name")
parser.add_argument('-l','--location', help = "Location")
parser.add_argument('-o','--organisation',help = "Organisation")
args = parser.parse_args()

fil = open('search_words.txt','w')
fil.write(args.first-last)
fil.write(args.location)
fil.write(args.organisation)
fil.close()

cmd = 'GoogleScraper -m http --keyword-file search_words.txt --num-workers 5 --search-engines "duckduckgo,google,bing,yahoo" --output-filename threaded-results.json -v debug'

json_file = open('threaded-results.json')
json_str = json_file.read()
json_parsed = json.loads(json_str)

f = open('csv_input.csv','w')
csv_writer = csv.writer(f)
count = 0
for result in json_parsed['results']
    if count == 0:
        header = result.keys()
        csvwriter.writerow(header)
        count+= 1
    csvwriter.writerow(result.values())
f.close()
