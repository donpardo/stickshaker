#!/usr/bin/env python
import sys
import os
import re # regular expressions
import shutil

# my_style should be put in a file later so it can be 
# set by the user
my_style = { " the ":" The ", " and ":" and ", " & ":" and ", "_":" " }

# DATA_ROOT = '/Users/matt/Stickshaker/data'
DATA_ROOT = '/nethome/mhanes/Personal/Stickshaker/data'
# MUSIC_ROOT = '/Users/matt/Stickshaker/music_test/music_dirs'
MUSIC_ROOT = '/nethome/mhanes/Personal/Stickshaker/music_test/music_dirs'
DATA_FILE = 'moves'
FULL_PATH = os.path.join(DATA_ROOT,DATA_FILE)
EXCEPT_DIR = os.path.join(MUSIC_ROOT,"EXCEPTIONS")
CHECKME = os.path.join(MUSIC_ROOT,"CHECKME")

# check that MUSIC_ROOT exists and is a directory
# check that DATA_FILE exists
# check that all folders on left in moves file exist
# allow wildcards on left side of moves (example: Bob Dylan*:::Bob Dylan)

def my_SetStyle(CHNG_LOC):
    # This function cleans up and standardizes the name of the 
    # destination folder (DEST_LOC), using the values set in 
    # my_style above.
    for my_target in my_style:
        my_replacement = re.compile(re.escape(my_target), re.IGNORECASE)
        CHNG_LOC = my_replacement.sub(my_style[my_target], CHNG_LOC)
        CHNG_LOC = re.sub(' +', ' ', CHNG_LOC)
    return CHNG_LOC

with open(FULL_PATH, "r") as MOVE_LINE:
    for LINE in MOVE_LINE:
        # get the two locations
        ORIG_LOC, DEST_LOC = LINE.split(":::")
        # remove trailing whitespace
        ORIG_LOC = ORIG_LOC.rstrip()
        # OG_ORIG is the OG original directory, needed below
        OG_ORIG_LOC=ORIG_LOC
        ORIG_LOC = os.path.join(MUSIC_ROOT,ORIG_LOC)
        DEST_LOC = DEST_LOC.rstrip()
        print("Original location = " + ORIG_LOC)
        # set the destination per style
        DEST_LOC = my_SetStyle(DEST_LOC)
        DEST_LOC = os.path.join(MUSIC_ROOT,DEST_LOC)
        print("Destination location = " + DEST_LOC) 
        print('Moving "' + ORIG_LOC + '" to "' + DEST_LOC +'"')
        
        # get the last character of the destination
        my_LastChar = DEST_LOC[-1:]
        # If the destination has a trailing slash, the original
        # directory gets put under the destination
        if my_LastChar == '/':
            DEST_LOC = os.path.join(DEST_LOC,OG_ORIG_LOC)

        # Make the destination directory 
        if not os.path.isdir(DEST_LOC):
           os.makedirs(DEST_LOC)

        # Move the files from the original to the destination
        #
        # Do not overwrite files in the destination. If there's a 
        # conflict, move the files to the exception directory
        my_files = os.listdir(ORIG_LOC)
        ORIG_LOC = ORIG_LOC + "/"
        DEST_LOC = DEST_LOC + "/"
        #print (ORIG_LOC)
        #print (DEST_LOC)
        for f in my_files:
            try:
                shutil.move(ORIG_LOC+f, DEST_LOC)
            except:
                print ( "There was a problem moving " + ORIG_LOC+f + " to " + DEST_LOC )
                print ( ORIG_LOC+f + " will be moved to EXCEPTIONS directory" )
                if not os.path.isdir(EXCEPT_DIR + ORIG_LOC):
                    try:
                        os.makedirs(EXCEPT_DIR + ORIG_LOC)
                    except:
                        print ("Parent exists under " + EXCEPT_DIR)
                    try:
                        shutil.move(ORIG_LOC+f, EXCEPT_DIR + ORIG_LOC)
                    except:
                        print ("Something is wrong. " + ORIG_LOC + "  couldn't be made under EXCEPTIONS." )
                        print ("Exiting.")
                        sys.exit(253)

        # Delete the original if it's empty. If it's not empty, 
        # move the original to the folder "CHECKME" to be, you know, 
        # checked. 
        if not os.listdir(ORIG_LOC): 
            try:
                os.rmdir(ORIG_LOC)
            except:
                print ("Could not remove " + ORIG_LOC + ".")
                print ("Moving to CHECKME directory.")
                if not os.path.isdir(CHECKME):
                    try:
                        os.makedirs(CHECKME)
                    except:
                        print ("Something is wrong. CHECKME couldn't be made.")
                        print ("Exiting.")
                        sys.exit(254)
                try:
                    shutil.move(ORIG_LOC, CHECKME)
                except:
                    print ("Something is wrong. Couldn't move " + ORIG_LOC + " under CHECKME.")
                    print ("Exiting.")
                    sys.exit(252)

