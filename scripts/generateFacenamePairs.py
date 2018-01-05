#!/usr/bin/python

import random
import os
import re
import csv
import copy
import sys

random.seed()

STIMULI_FOLDER = os.path.abspath('../stimuli')
TOTAL_BLOCKS = 6
KNOWN_BLOCKS = TOTAL_BLOCKS / 2
NOVEL_BLOCKS = TOTAL_BLOCKS / 2
TRIALS_PER_BLOCK = 6
TOTAL_UNIQUE_STIMULI = TRIALS_PER_BLOCK * (NOVEL_BLOCKS + 1)

# get the run number/id
run = sys.argv[1]

# load stims into lists
with open('names/female.txt','r') as fh:
    fnames = [name.rstrip('\n') for name in fh]

with open('names/male.txt','r') as fh:
    mnames = [name.rstrip('\n') for name in fh]

# stimuli lists
fstim = list()
mstim = list()

for stim in os.listdir(STIMULI_FOLDER):
    if re.match(r'^CFD-WM',stim):
        mstim.append(stim)
    else:
        fstim.append(stim)

# random stimuli lists
rfstims = list()
rmstims = list()

# get 12 random of each gender
for i in range(0, TOTAL_UNIQUE_STIMULI):
    f=fstim[random.randrange(0,len(fstim))]
    fstim.remove(f)
    rfstims.append(f)
    m=mstim[random.randrange(0,len(mstim))]
    mstim.remove(m)
    rmstims.append(m)

# random name lists
rfnames = list()
rmnames = list()

# get 12 random of each gender
for i in range(0, TOTAL_UNIQUE_STIMULI):
    f=fnames[random.randrange(0,len(fnames))]
    fnames.remove(f)
    rfnames.append(f)
    m=mnames[random.randrange(0,len(mnames))]
    mnames.remove(m)
    rmnames.append(m)

fpairs = [list(pair) for pair in zip(rfstims,rfnames)]
mpairs = [list(pair) for pair in zip(rmstims,rmnames)]

novelBlocks = list()
# create groups of 6 for the novel blocks
for i in range(0, NOVEL_BLOCKS):
    # deepcopy because we have embedded lists!
    females = copy.deepcopy(fpairs[i * (TRIALS_PER_BLOCK / 2):(i + 1)*(TRIALS_PER_BLOCK / 2)])
    males   = copy.deepcopy(mpairs[i * (TRIALS_PER_BLOCK / 2):(i + 1)*(TRIALS_PER_BLOCK / 2)])
    novelBlocks.append(females + males)
    random.shuffle(novelBlocks[-1])

knownBlocks = list()
for i in range(0, KNOWN_BLOCKS):
    # get our stims
    # deepcopy because we have embedded lists!
    males = copy.deepcopy(mpairs[-1 * (TRIALS_PER_BLOCK / 2):])
    females = copy.deepcopy(fpairs[-1 * (TRIALS_PER_BLOCK / 2):])
    # assign a random 'fake' name from the other stim of same gender
    for j in range(0, TRIALS_PER_BLOCK / 2):
        fn=females[(j+random.randrange(1,TRIALS_PER_BLOCK/2))%(TRIALS_PER_BLOCK/2)][1]
        mn=males[(j+random.randrange(1,TRIALS_PER_BLOCK/2))%(TRIALS_PER_BLOCK/2)][1]
        females[j].append(fn)
        males[j].append(mn)
        print(females[j][1:])
    knownBlocks.append(males+females)
    males = []
    females = []
    random.shuffle(knownBlocks[-1])

# create csv files
for i in range(0, TOTAL_BLOCKS, 2):
    # write the novel block
    with open('r'+run+'b'+str(i)+'.csv', 'w') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(['image','name'])
        for trial in novelBlocks[i/2]:
            writer.writerow(list(trial))

    # write the known block
    with open('r'+run+'2b'+str(i+1)+'.csv', 'w') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(['image','name1','name2','corr'])
        for trial in knownBlocks[i/2]:
            corr = random.randrange(0,2)
            names = trial[1:]
            writer.writerow([trial[0],names[corr],names[(1 + corr) % 2],corr])

# write a final run
with open('run'+run+'.csv','w') as fh:
    writer = csv.writer(fh, delimiter=',')
    writer.writerow(['blockFile','isKnown','isNovel'])
    isKnown = 0
    for i in range(0, TOTAL_BLOCKS):
        writer.writerow(['facename/blocks/r2b'+str(i)+'.csv', isKnown, (isKnown + 1) % 2])
        isKnown = (isKnown + 1) % 2
