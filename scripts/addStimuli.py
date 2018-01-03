#!/usr/bin/python

# take a list of 'trial' csv's and randomly assign stimuli to each one
import sys
import csv
import random
import os

random.seed()

stimuliFolder = os.path.abspath(sys.argv[1])
csvList = sys.argv[2:]

stimuliList = os.listdir(stimuliFolder)

for c in csvList:
    # read the csv into a list of dicts
    rowList = list()
    with open(c) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rowList.append(dict(row))
    
    # select 6 random stimuli
    stimuli = list()
    for i in range(0,6):
        stim = stimuliList[random.randrange(0,len(stimuliList))]
        stimuliList.remove(stim)
        stimuli.append(stim)

    # replace stimuli in the dicts
    for row in rowList:
        row['Stimulus'] = stimuli[int(row['Stimulus'])-1]

    # write to file
    with open('new_'+c,'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = rowList[0].keys())
        writer.writeheader()
        for row in rowList:
            writer.writerow(row)

