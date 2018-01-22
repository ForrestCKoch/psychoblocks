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

# CORERCT + INCORRECT_KNOWN + INCORRECT_NOVEL = 1.0
# % of correct responses for known trials
CORRECT = 0.5
# % of incorrect responses with known names
INCORRECT_KNOWN = 0.25
# % of incorrect responses with novel names
INCORRECT_NOVEL = 0.25

STIMULI_FOLDER = os.path.abspath('../stimuli')
# total number of runs to be created
RUNS = 5
# total number of blocks per run
# NB: must be even for balancing novel/known blocks
BLOCKS = 8
# number of known blocks per run
KNOWN = BLOCKS / 2
# number of novel blocks per run
NOVEL = BLOCKS / 2
# number of trails per block
# NB: must be even for gender balancing
TRIALS = 4
# number of unique known stimuli throughout experiment
KNOWN_STIMULI = 6
# number of unique stimuli used throughout experiment
UNIQUE_STIMULI = KNOWN_STIMULI + (RUNS * NOVEL * TRIALS)
# number of extra names needed for known stimuli trials
EXTRA_NAMES = int(RUNS * TRIALS * KNOWN * INCORRECT_NOVEL)

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

# random stimuli lists
rand_female_stimulis = list()
rand_male_stimulis = list()

# random stimuli of each gender (50%)
for i in range(0, UNIQUE_STIMULI/2):
    f = female_stimuli[random.randrange(0,len(female_stimuli))]
    female_stimuli.remove(f)
    rand_female_stimulis.append(f)
    m = male_stimuli[random.randrange(0,len(male_stimuli))]
    male_stimuli.remove(m)
    rand_male_stimulis.append(m)

# random name lists
rand_female_names = list()
rand_male_names = list()

# random names of each gender (50%) 
for i in range(0, UNIQUE_STIMULI/2):
    f = female_names[random.randrange(0,len(female_names))]
    female_names.remove(f)
    rand_female_names.append(f)
    m = male_names[random.randrange(0,len(male_names))]
    male_names.remove(m)
    rand_male_names.append(m)

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
    copy_males = copy.deepcopy(known_males)
    copy_females = copy.deepcopy(known_females)
    # keep track of how many times each stimulus is used
    used = dict()
    # keep track of correct choices
    cor_fem = 0
    cor_mal = 0
    # keep track of incorrect known choices
    inc_fem_known = 0
    inc_mal_known = 0
    # keep track of incorrect novel choices
    inc_fem_novel = 0
    inc_mal_novel = 0

    max_cor = int(TRIALS * KNOWN * CORRECT / 2)
    max_inc_known = int(TRIALS * KNOWN * INCORRECT_KNOWN / 2)
    max_inc_novel = int(TRIALS * KNOWN * INCORRECT_NOVEL / 2)

    for j in copy_males:
        used[j[1]] = 0
    for j in copy_females:
        used[j[1]] = 0
    known_blocks = list()
    for j in range(0, KNOWN):
        block = list()
        for k in range(0, TRIALS / 2):
            # chose a random male and a random female
            m = copy_males[random.randrange(0,len(copy_males))]
            f = copy_females[random.randrange(0,len(copy_females))]

            # increment dictionary values
            used[m[1]] += 1
            used[f[1]] += 1
            # check that we haven't hit use limit
            if used[m[1]] == TRIALS:
                copy_males.remove(m)
            if used[f[1]] == TRIALS:
                copy_females.remove(f)
            # stupid bloody python with it's stupid bloody copying....
            m = copy.deepcopy(m)
            f = copy.deepcopy(f)
            # randomize names of each and record correctness
            rand = random.random()
            if ((rand < CORRECT) or ((inc_mal_novel >= max_inc_novel) and (inc_mal_known == max_inc_known))) and (cor_mal < max_cor):
                # don't change, the name is correct
                m.append('yes')
                cor_mal += 1
            elif ((rand < CORRECT + INCORRECT_KNOWN) or (inc_mal_novel == max_inc_novel)) and (inc_mal_known < max_inc_known) :
                # pick a random name from other known names
                name = known_males[random.randrange(0,len(known_males))][1]
                while(name == m[1]):
                    name = known_males[random.randrange(0,len(known_males))][1]
                m[1] = name
                m.append('no')
                inc_mal_known += 1
            else:
                # pick a random name from extras
                name = extra_male_names[random.randrange(0,len(extra_male_names))]
                extra_male_names.remove(name)
                m[1] = name
                m.append('no')
                inc_mal_novel += 1 
                if(inc_mal_novel > max_inc_novel):
                    print(inc_mal_known)
                    print(cor_mal)
                    exit()
            # and for females...
            rand = random.random()
            if ((rand < CORRECT) or ((inc_fem_novel >= max_inc_novel) and (inc_fem_known == max_inc_known))) and (cor_fem < max_cor):
                # don't change, the name is correct
                f.append('yes')
                cor_fem += 1
            elif ((rand < CORRECT + INCORRECT_KNOWN) or (inc_fem_novel == max_inc_novel)) and (inc_fem_known < max_inc_known) :
                # pick a random name from other known names
                name = known_females[random.randrange(0,len(known_females))][1]
                while(name == f[1]):
                    name = known_females[random.randrange(0,len(known_females))][1]
                f[1] = name
                f.append('no')
                inc_fem_known += 1
            else:
                # pick a random name from extras
                name = extra_female_names[random.randrange(0,len(extra_female_names))]
                extra_female_names.remove(name)
                f[1] = name
                f.append('no')
                inc_fem_novel += 1
            # and add to the block
            block.append(m)
            block.append(f)
        random.shuffle(block)
        known_blocks.append(block)
    known_runs.append(known_blocks)
 
# create runs
runlist = list()
for i in range(0, RUNS):
    n = copy.deepcopy(novel_blocks[i * NOVEL:(i+1) * NOVEL])
    k = copy.deepcopy(known_runs[i])
    n = zip(n,['novel']*len(n))
    k = zip(k,['known']*len(k))
    
    x = list(n+k)
    random.shuffle(x)    

    runlist.append(x)

    
for i in range(0, RUNS):
    # write our runfile
    with open('r'+run+'-'+str(i)+'.csv','w') as r:
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
            runwriter.writerow(['facename/blocks/r'+run+'-'+str(i)+'b'+str(j)+'.csv',isKnown,(isKnown+1)%2]) 
            with open('r'+run+'-'+str(i)+'b'+str(j)+'.csv','w') as b:
                blockwriter = csv.writer(b,delimiter=',')
                blockwriter.writerow(['image','name','corr'])
                for trial in block:
                    blockwriter.writerow(trial[0])
