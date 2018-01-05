import random 
import copy

random.seed()

KNOWN_BLOCKS = 3
TRIALS_PER_BLOCK = 6

fpairs = [list(pair) for pair in zip(range(0,12),range(0,12))]
knownBlocks = list()

for i in range(0, 3):
    # get our stims
    females = copy.deepcopy(fpairs[-1 * (TRIALS_PER_BLOCK / 2):])
    # assign a random 'fake' name from the other stim of same gender
    for j in range(0, TRIALS_PER_BLOCK / 2):
        fn = females[(j+random.randrange(1,TRIALS_PER_BLOCK / 2)) % (TRIALS_PER_BLOCK / 2)][1]
        females[j].append(fn)
    knownBlocks.append(list(females))
    print(females[0][1:])
    females = []
    random.shuffle(knownBlocks[-1])
