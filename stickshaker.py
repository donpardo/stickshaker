#!/usr/bin/env python
import sys
import os
import re # regular expressions

# my_subs should be put in a file later so it can be 
# set by the user
my_subs = { " the ":" The ", " and ":" and ", " & ":" and ", "_":" " }

DATA_ROOT = '/Users/matt/Stickshaker/data'
DATA_FILE = 'moves'
MUSIC_ROOT = '/Users/matt/Stickshaker/music_test'

def articleSub(CHNG_LOC):
    for my_target in my_subs:
        my_replacement = re.compile(re.escape(my_target), re.IGNORECASE)
        CHNG_LOC = my_replacement.sub(my_subs[my_target], CHNG_LOC)
        CHNG_LOC = re.sub(' +', ' ', CHNG_LOC)
    return CHNG_LOC

FULL_PATH=os.path.join(DATA_ROOT,DATA_FILE)

with open(FULL_PATH, "r") as MOVE_LINE:
    for LINE in MOVE_LINE:
        ORIG_LOC, DEST_LOC = LINE.split(":::")
        ORIG_LOC = ORIG_LOC.rstrip()
        DEST_LOC = DEST_LOC.rstrip()
        #print("Original location = " + ORIG_LOC)
        DEST_LOC = articleSub(DEST_LOC)
        #print("Destination location = " + DEST_LOC) 
        print('Moving "' + ORIG_LOC + '" to "' + DEST_LOC +'"')
        # os.rename("ORIG_LOC", "DEST_LOC")
        
