#!/usr/bin/python3

# convert csv to have 'generic' stimuli values
import sys
import csv

stimDict = dict()
copy = list()
count = 1

with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Stimulus'] not in stimDict:
            stimDict[row['Stimulus']]=count
            count += 1
        copy.append(dict(row))
        copy[-1]['Stimulus'] = stimDict[row['Stimulus']]
        copy[-1].pop('Weight', None)
        copy[-1].pop('StimType', None)

with open('conv_'+sys.argv[1],'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=copy[0].keys())
    writer.writeheader()
    for row in copy:
        writer.writerow(row)
        
