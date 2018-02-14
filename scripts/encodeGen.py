#!/usr/bin/python

import random
import os
import re
import csv
import copy
import sys

def usage():
    sys.stderr.write('Usage: '+sys.argv[0]+" [runid]\n")
    exit()

# check usage
if len(sys.argv) != 2:
    usage()

random.seed()

"""
# CORERCT + INCORRECT_KNOWN + INCORRECT_NOVEL = 1.0
# % of correct responses for known trials
CORRECT = 0.5
# % of incorrect responses with known names
INCORRECT_KNOWN = 0.25
# % of incorrect responses with novel names
INCORRECT_NOVEL = 0.25
"""

STIMULI_FOLDER = os.path.abspath('../stimuli')
# total number of runs to be created
RUNS = 2
# total number of blocks per run
# NB: must be even for balancing novel/known blocks
BLOCKS = 4
# number of known blocks per run
KNOWN = int(BLOCKS / 2)
# number of novel blocks per run
NOVEL = int(BLOCKS / 2)
# number of trails per block
# NB: must be even for gender balancing
TRIALS = 8
# number of unique known stimuli throughout experiment
KNOWN_STIMULI = 2
# number of unique stimuli used throughout experiment
UNIQUE_STIMULI = KNOWN_STIMULI + (RUNS * NOVEL * TRIALS)
# number of extra names needed for known stimuli trials
#EXTRA_NAMES = int(RUNS * TRIALS * KNOWN * INCORRECT_NOVEL)

# get the run number/id
run = sys.argv[1]

# load stims into lists
with open('names/female.txt','r') as fh:
    female_names = [name.rstrip('\n') for name in fh]

with open('names/male.txt','r') as fh:
    male_names = [name.rstrip('\n') for name in fh]

# stimuli lists
female_stimuli = list()
male_stimuli = list()

for stim in os.listdir(STIMULI_FOLDER):
    if re.match(r'^CFD-WM',stim):
        male_stimuli.append(stim)
    else:
        female_stimuli.append(stim)

for scan in ['s1','s2']:

        # random stimuli lists
        rand_female_stimulis = list()
        rand_male_stimulis = list()

        # random stimuli of each gender (1:1 m:f)
        for i in range(0, int(UNIQUE_STIMULI/2)):
            f = female_stimuli[random.randrange(0,len(female_stimuli))]
            female_stimuli.remove(f)
            rand_female_stimulis.append(f)
            m = male_stimuli[random.randrange(0,len(male_stimuli))]
            male_stimuli.remove(m)
            rand_male_stimulis.append(m)

        # random name lists
        rand_female_names = list()
        rand_male_names = list()

        # random names of each gender (1:1 m:f) 
        for i in range(0, int(UNIQUE_STIMULI/2)):
            f = female_names[random.randrange(0,len(female_names))]
            female_names.remove(f)
            rand_female_names.append(f)
            m = male_names[random.randrange(0,len(male_names))]
            male_names.remove(m)
            rand_male_names.append(m)

        """
        # get our extra names for known trials
        extra_female_names = list()
        extra_male_names = list()
        for i in range(0,EXTRA_NAMES/2):
            f = female_names[random.randrange(0,len(female_names))]
            female_names.remove(f)
            extra_female_names.append(f)
            m = male_names[random.randrange(0,len(male_names))]
            male_names.remove(m)
            extra_male_names.append(m)
        """
            
        # generate unique names for each stimuli
        female_pairs = [list(pair) for pair in zip(rand_female_stimulis, rand_female_names)]
        male_pairs = [list(pair) for pair in zip(rand_male_stimulis, rand_male_names)]


        novel_blocks = list()
        # create groups for the novel blocks
        for i in range(0, NOVEL * RUNS):
            # copy over 
            # deepcopy because we have embedded lists!
            females = copy.deepcopy(female_pairs[i * (TRIALS / 2):(i + 1)*(TRIALS / 2)])
            males   = copy.deepcopy(male_pairs[i * (TRIALS / 2):(i + 1)*(TRIALS / 2)])
            novel_blocks.append(females + males)
            random.shuffle(novel_blocks[-1])


        # get our known stims
        # deepcopy because we have embedded lists!
        known_males = copy.deepcopy(male_pairs[-1 * (KNOWN_STIMULI / 2):])
        known_females = copy.deepcopy(female_pairs[-1 * (KNOWN_STIMULI / 2):])

        known_runs = list()

        # we need to do this for each run to keep things balanced
        for i in range(0, RUNS):
            known_blocks = list()
            for j in range(0, KNOWN):
                block = list()
                last = None
                # within each block, randomly cycle through
                # known subjects 1 at a time
                for x in range(0, TRIALS / KNOWN_STIMULI):
                    copy_known = copy.deepcopy(known_males) + copy.deepcopy(known_females)
                    random.shuffle(copy_known)
                    for k in range(0, KNOWN_STIMULI):
                        # chose a random subject
                        subject = copy_known.pop()
                        if subject == last:
                            subject = copy_known.pop()
                            copy_known.append(last)
                            random.shuffle(copy_known)
                        last = subject
                        # and add to the block
                        block.append(subject)
                known_blocks.append(block)
            known_runs.append(known_blocks)
         
        # create runs
        runlist = list()
        for i in range(0, RUNS):
            n = copy.deepcopy(novel_blocks[i * NOVEL:(i+1) * NOVEL])
            k = copy.deepcopy(known_runs[i])
            n = zip(n,['novel']*len(n))
            k = zip(k,['known']*len(k))
            
            x = list()
            for j in range(0,KNOWN):
                x.append(n[j])
                x.append(k[j])

            runlist.append(x)

        for i in range(0, RUNS):
            # write our runfile
            with open(scan+'r'+run+'-'+str(i)+'.csv','w') as r:
                runwriter = csv.writer(r, delimiter=',')
                # setup the entries expected
                runwriter.writerow(['blockFile','isKnown','isNovel'])
                # cycle through each block in the run
                for j in range(0,len(runlist[i])):
                    block = runlist[i][j]
                    if block[1] == 'novel':
                        isKnown = 0
                    else:
                        isKnown = 1
                    # write the block info
                    runwriter.writerow(['encodefn/blocks/'+scan+'r'+run+'-'+str(i)+'b'+str(j)+'.csv',isKnown,(isKnown+1)%2]) 
                    with open(scan+'r'+run+'-'+str(i)+'b'+str(j)+'.csv','w') as b:
                        blockwriter = csv.writer(b,delimiter=',')
                        blockwriter.writerow(['image','name','corr'])
                        for trial in block[0]:
                            blockwriter.writerow(trial)
