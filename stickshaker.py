#!/usr/bin/env python
import sys
import os
import re # regular expressions
import shutil

# my_subs should be put in a file later so it can be 
# set by the user
my_subs = { " the ":" The ", " and ":" and ", " & ":" and ", "_":" " }

DATA_ROOT = '/Users/matt/Stickshaker/data'
DATA_FILE = 'moves'
MUSIC_ROOT = '/Users/matt/Stickshaker/music_test'
EXCEPT_DIR = MUSIC_ROOT + "/EXCEPTIONS"
CHECKME = MUSIC_ROOT + "/CHECKME"

def my_SetStyle(CHNG_LOC):
    # This funtion cleans up and standardizes the name of the 
    # destination folder (DEST_LOC), using the values set in 
    # my_subs above.
    for my_target in my_subs:
        my_replacement = re.compile(re.escape(my_target), re.IGNORECASE)
        CHNG_LOC = my_replacement.sub(my_subs[my_target], CHNG_LOC)
        CHNG_LOC = re.sub(' +', ' ', CHNG_LOC)
    return CHNG_LOC

FULL_PATH=os.path.join(DATA_ROOT,DATA_FILE)

with open(FULL_PATH, "r") as MOVE_LINE:
    for LINE in MOVE_LINE:
        # get the two locations
        ORIG_LOC, DEST_LOC = LINE.split(":::")
        # remove trailing whitespace
        ORIG_LOC = ORIG_LOC.rstrip()
        DEST_LOC = DEST_LOC.rstrip()
        #print("Original location = " + ORIG_LOC)
        # set the destination per style
        DEST_LOC = my_SetStyle(DEST_LOC)
        #print("Destination location = " + DEST_LOC) 
        print('Moving "' + ORIG_LOC + '" to "' + DEST_LOC +'"')
        os.rename("ORIG_LOC", "DEST_LOC")
        # get the last character of the destination
        my_LastChar = DESTLOC[-1:]
        # If the destination has a trailing slash, the original
        # directory gets put under the destination
        if my_LastChar == '/':
            DEST_LOC = DEST_LOC + ORIG_LOC

        # Make the destination directory 
        if not os.path.isdir(DEST_LOC):
           os.makedirs(DEST_LOC)

        # Move the files from the original to the destination
        #
        # Do not overwrite files in the destination. If there's a 
        # conflict, move the files to the exception directory
        my_files = os.listdir(ORIG_LOC)
        for f in my_files:
            shutil.move(ORIG_LOC+f, DESTLOC)
            except:
                print ("There was a problem moving " + ORIG_LOC+f + " to " + DESTLOC".")
                print (ORIG_LOC+f " will be moved to EXCEPTIONS directory")
                if not os.path.isdir(EXCEPT_DIR + ORIG_LOC)
                    os.makedirs(EXCEPT_DIR + ORIG_LOC)
                    except:
                        print "Parent exists under " + EXCEPT_DIR)
                    shutil.move(ORIG_LOC+f, EXCEPT_DIR + ORIG_LOC)
                        except:
                            print ("Something is wrong. " + ORIG_LOC + "  couldn't be made under EXCEPTIONS.")
                            print ("Exiting.")
                            sys.exit(253)

        # Delete the original if it's empty. If it's not empty, 
        # move the original to the folder "CHECKME" to be, you know, 
        # checked. 
        if not os.listdir(ORIG_LOC): 
            os.rmdir(ORIG_LOC, *, dir_fd=None)
            except:
                print ("Could not remove " + ORIG_LOC + "."
                print ("Moving to CHECKME directory.")
                if not os.path.isdir(CHECKME)
                    os.makedirs(CHECKME)
                    except:
                        print ("Something is wrong. CHECKME couldn't be made.")
                        print ("Exiting.")
                        sys.exit(254)
                shutil.move(ORIG_LOC, CHECKME)
                        except:
                            print ("Something is wrong. Couldn't move " + ORIG_LOC + " under CHECKME.")
                            print ("Exiting.")
                            sys.exit(252)

