#!/usr/bin/python

import random
import os
import re
import csv
import copy
import sys

random.seed()

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

# load stims into lists
with open('names/female.txt','r') as fh:
    female_names = [name.rstrip('\n') for name in fh]

with open('names/male.txt','r') as fh:
    male_names = [name.rstrip('\n') for name in fh]

# stimuli lists
female_stimuli = list()
male_stimuli = list()

# load images into their correct gender list
for stim in os.listdir(STIMULI_FOLDER):
    if re.match(r'^CFD-WM',stim):
        male_stimuli.append(stim)
    else:
        female_stimuli.append(stim)

# shuffle the stimuli
random.shuffle(female_names)
random.shuffle(male_names)
random.shuffle(female_stimuli)
random.shuffle(male_stimuli)

# create both initial and follow-up sets
for scan in ['s0','s1']:

    # random stimuli lists
    rand_female_stimulis = list()
    rand_male_stimulis = list()
    # random name lists
    rand_female_names = list()
    rand_male_names = list()

    # random stimuli of each gender (1:1 m:f)
    for i in range(0, int(UNIQUE_STIMULI/2)):
        rand_female_stimulis.append(female_stimuli.pop())
        rand_male_stimulis.append(male_stimuli.pop())
        rand_female_names.append(female_names.pop())
        rand_male_names.append(male_names.pop())
        
    # generate unique names for each stimuli
    female_pairs = [list(pair) for pair in zip(rand_female_stimulis, rand_female_names)]
    male_pairs = [list(pair) for pair in zip(rand_male_stimulis, rand_male_names)]

    # create groups for the novel blocks
    novel_blocks = list()
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

    # create repeated blocks
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
        with open(scan+'r'+str(i)+'.csv','w') as r:
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
                runwriter.writerow(['data/blocks/'+scan+'r'+str(i)+'b'+str(j)+'.csv',isKnown,(isKnown+1)%2]) 
                with open(scan+'r'+str(i)+'b'+str(j)+'.csv','w') as b:
                    blockwriter = csv.writer(b,delimiter=',')
                    blockwriter.writerow(['image','name','corr'])
                    for trial in block[0]:
                        blockwriter.writerow(trial)

    # now to create the post-scan test
    test_male_pairs = copy.deepcopy(male_pairs)
    test_female_pairs = copy.deepcopy(female_pairs)
    test_male_names = copy.deepcopy(male_names)
    test_female_names = copy.deepcopy(female_names)
    # shuffle the lists
    random.shuffle(test_male_pairs)
    random.shuffle(test_male_names)
    random.shuffle(test_female_pairs)
    random.shuffle(test_female_names)

    # create a list of 'trials'
    test_trials = list()
    while(len(test_male_pairs) and len(test_female_pairs)):
        if random.choice([True,False]):
            # add a male to the trial
            pair = test_male_pairs.pop()
            false_name = test_male_names.pop()
            if false_name == pair[1]:
                tmp = test_male_names.pop()
                test_male_names.append(name)
                random.shuffle(test_male_names)
                false_name = tmp
        else:
            # add a female to the trial
            pair = test_female_pairs.pop()
            false_name = test_female_names.pop()
            if false_name == pair[1]:
                tmp = test_female_names.pop()
                test_female_names.append(name)
                random.shuffle(test_female_names)
                false_name = tmp

        # randomize the name order
        if random.choice([True,False]):
            # correct name on left
            test_trials.append([pair[0],pair[1],false_name,'left'])
        else:
            # correct name on right
            test_trials.append([pair[0],false_name,pair[1],'right'])

    # finish off the remaining genders
    while(len(test_male_pairs)):
        # add a male to the trial
        pair = test_male_pairs.pop()
        false_name = test_male_names.pop()
        if false_name == pair[1]:
            tmp = test_male_names.pop()
            test_male_names.append(name)
            random.shuffle(test_male_names)
            false_name = tmp
        # randomize the name order
        if random.choice([True,False]):
            # correct name on left
            test_trials.append([pair[0],pair[1],false_name,'left'])
        else:
            # correct name on right
            test_trials.append([pair[0],false_name,pair[1],'right'])
    while(len(test_female_pairs)):
        # add a female to the trial
        pair = test_female_pairs.pop()
        false_name = test_female_names.pop()
        if false_name == pair[1]:
            tmp = test_female_names.pop()
            test_female_names.append(name)
            random.shuffle(test_female_names)
            false_name = tmp
        # randomize the name order
        if random.choice([True,False]):
            # correct name on left
            test_trials.append([pair[0],pair[1],false_name,'left'])
        else:
            # correct name on right
            test_trials.append([pair[0],false_name,pair[1],'right'])
     
    # write the trials to a csv
    with open('test_recall.csv','w') as fh:
        fh.write("image,lname,rname,correct\n")
        for trial in test_trials:
            fh.write(trial[0]+","+trial[1]+","+trial[2]+","+trial[3]+"\n")


    # and let's store the stimuli information to a summary file for easy reference
    with open('StimuliSummary.txt','w') as fh:
        for i in range(0,len(male_pairs)-(KNOWN_STIMULI/2)):
            fh.write(male_pairs[i][0]+","+male_pairs[i][1]+",novel\n")
            fh.write(female_pairs[i][0]+","+female_pairs[i][1]+",novel\n")
        for i in range(len(male_pairs)-(KNOWN_STIMULI/2),len(male_pairs)):
            fh.write(male_pairs[i][0]+","+male_pairs[i][1]+",repeated\n")
            fh.write(female_pairs[i][0]+","+female_pairs[i][1]+",repeated\n")

    
