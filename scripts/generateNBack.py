#!/usr/bin/python

# This script will randomly generate an n back trial
# with 6 non lures, 2 lures, and 2 targets
# stimuli value will be between 1 and 6 inclusive
import sys
import csv
import random

NUM_TARGETS = 2
NUM_LURES = 2

random.seed()

nback = int(sys.argv[1])
outfile = sys.argv[2]

# used for stimuli placement
block = [None] * 10
# used to keep track of remaining spots
spots = range(0,10)

# initialize first stimuli value
stimuli = 1

# create a truncated list for target placement selection
targetList = spots[:-1*nback]
# place targets
for i in range(0,NUM_TARGETS):
    value = targetList[random.randrange(0,len(targetList))]
    # remove value from potential lists
    targetList.remove(value)
    spots.remove(value)
    # remove the second occurence from spots, and targetList if necessary
    spots.remove(value+nback)
    if value+nback in targetList:
        targetList.remove(value+nback)
    if value-nback in targetList:
        targetList.remove(value-nback)
    # set the value within the block
    block[value] = (stimuli,'nonlure')
    block[value+nback] = (stimuli,'target')
    # increment the stimuli value
    stimuli += 1

# now to place two lures
for i in range(0,NUM_LURES):
    # randomly select one value
    fvalue = spots[random.randrange(0,len(spots))]
    # create a temporary copy for second random selection
    tmpList = list(spots)
    tmpList.remove(fvalue)
    if fvalue+nback in tmpList:
        tmpList.remove(fvalue+nback)
    if fvalue-nback in tmpList:
        tmpList.remove(fvalue-nback)
    # note this second random selection can come either before or after
    # the first selected value
    svalue = tmpList[random.randrange(0,len(tmpList))]
    if fvalue>svalue:
        block[fvalue] = (stimuli,'lure')
        block[svalue] = (stimuli,'nonlure')
    else:
        block[svalue] = (stimuli,'lure')
        block[fvalue] = (stimuli,'nonlure')
    spots.remove(fvalue)
    spots.remove(svalue)
    stimuli += 1

for i in range(0, len(block)):
    if not block[i]:
        block[i] = (stimuli,'nonlure')
        stimuli += 1 

print(block)

with open(outfile,'w') as csvfile:
    fieldnames =['TargetType','CorrectResponse','Stimulus','BlockType']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for trial in block:
        tmp = dict()
        tmp['TargetType'] = trial[1]
        tmp['CorrectResponse'] = 1 if trial[1] == 'target' else 2
        tmp['Stimulus'] = trial[0]
        tmp['BlockType'] = '2-Back'
        writer.writerow(tmp)
