#!/usr/bin/env python
#
# Crudely reorganizes a music collection based on 
# the contents of a file described in the README

# TODOS:
# - Define appropriate variables in an external file
# - check that music_Root exists and is a directory
# - check that moveFileName exists. if not, allow user to select file interactively
# - check that all folders on left in moveFileName file exist. if not, abort.
# - allow wildcards on left side of moves (example: Bob Dylan*:::Bob Dylan/)
# - final pass to clean up directory names regardless of whether or not
#       they are in the moves file.
# - allow user to review, edit and supplement the my_style entries
# - create dry run similar to rsync

import sys
import os
import re # regular expressions
import shutil

# my_style should be put in a file later so it can be 
# set by the user
my_style = { " the ":" The ", " and ":" and ", " & ":" and ", "_":" ", " w ":" with " }

#music_Root = '/Users/matt/Stickshaker/music_test/music_dirs'
#data_Root = '/Users/matt/Stickshaker/data'
data_Root = '/nethome/mhanes/Personal/Stickshaker/data'
music_Root = '/nethome/mhanes/Personal/Stickshaker/music_test/music_dirs'
moveFileName = 'moves'
moveFilePath = os.path.join(data_Root,moveFileName)
exception_Dir = os.path.join(music_Root,"EXCEPTIONS")
check_Me = os.path.join(music_Root,"CHECKME")
my_Folders = dict()
my_BadDirs = list()

def func_SetStyle(my_ChngLoc):
    print("func_SetStyle successfully called")
    # This function cleans up and standardizes the name of the 
    # destination folder (loc_Dest), using the values set in 
    # my_style above.
    for my_target in my_style:
        my_replacement = re.compile(re.escape(my_target), re.IGNORECASE)
        my_ChngLoc = my_replacement.sub(my_style[my_target], my_ChngLoc)
        my_ChngLoc = re.sub(' +', ' ', my_ChngLoc)
    return my_ChngLoc

def func_MoveFiles(my_File, loc_Final):
    print("my_MOVEFILE successfully called")
    # Do not overwrite files in the destination. If there's a 
    # conflict, move the files to the exception directory
    try:
        shutil.move(my_File, loc_Final)
    except:
        print ( "There was a problem moving " + my_File + " to " + loc_Final )
        print ( my_File + " will be moved to EXCEPTIONS directory" )
        if not os.path.isdir(exception_Dir + loc_OG):
            try:
                os.makedirs(exception_Dir + loc_OG)
            except:
                print ("Parent exists under " + exception_Dir)
            try:
                shutil.move(loc_Orig+f, exception_Dir + loc_OG)
            except:
                print ("Something is wrong. " + loc_OG + "  couldn't be made under EXCEPTIONS." )
                print ("Skipping.")
    return                

def func_MoveTest(my_From,my_To):
    print("func_MoveTest successfully called.")
    print("From: " + my_From + "\nTo: " + my_To)
    print ("-------------")
    #
    # Test each of the contents of my_FROM to see if it is a
    # directory. If it is, create it in the destination then move down
    # one level and do it again. If it is a file, move it.
    #
    my_Files = os.listdir(my_From)
    print (my_Files)
    for M_F in my_Files:
        print("testing files under " + my_From)
        my_testPath = os.path.join(my_From,M_F)
        print (my_testPath)
        if os.path.isfile(my_testPath) and not os.path.islink(my_testPath):
            func_MoveFiles(my_testPath,my_To)
        if os.path.isdir(my_testPath) and not os.path.islink(my_testPath):
            func_MoveTest(my_testPath,my_To)
        print (my_testPath + " is not a directory or a file. Skipping.")
    return

# actual thing that does stuff follows.

with open(moveFilePath, "r") as my_MoveLine:
    for my_Line in my_MoveLine:
        # get the two locations
        loc_Orig, loc_Dest = my_Line.split(":::")
        loc_Orig = loc_Orig.rstrip()
        loc_Dest = loc_Dest.rstrip()
        #
        # get the last character of the destination
        #
        my_LastChar = loc_Dest[-1:]
        #
        # If the destination has a trailing slash, the original
        # directory gets put under the destination
        #
        if my_LastChar == '/':
            loc_Dest = os.path.join(loc_Dest,loc_Orig)
        #
        # set the destination per style
        #
        loc_Dest = func_SetStyle(loc_Dest)
        #
        # build destination directory full path
        #
        loc_Dest = os.path.join(music_Root,loc_Dest)
        loc_Orig = os.path.join(music_Root,loc_Orig)
        print('Moving: "' + loc_Orig + '"\n    to: "' + loc_Dest +'"')
        #
        # add to dictionary for use below
        #
        my_Folders[loc_Orig] = loc_Dest
        #
        # check if left side exists. note it if it does not.
        #
        if not os.path.isdir(loc_Orig):
            my_BadDirs.append(loc_Orig)
#
# alert the user, if needed
#
if my_BadDirs:
    print ("The following directories do not exist. You need to fix this before proceeding.")
    for my_Dir in my_BadDirs:
        print (my_Dir)
    sys.exit(254)
#
# Time to do the actual moves:
#
for loc_Orig in my_Folders:
    loc_Dest = my_Folders[loc_Orig]
    #
    # Make the destination directory 
    #
    if not os.path.isdir(loc_Dest):
       os.makedirs(loc_Dest)
    #
    # Move the files from the original to the destination
    #
    loc_Dest = loc_Dest + "/"
    loc_Orig = loc_Orig + "/"
    print ("ORIG: " + loc_Orig)
    print ("DEST: " + loc_Dest)
    print ("-------------")
    func_MoveTest(loc_Orig,loc_Dest)
    #
    # Delete the original if it's empty. If it's not empty, 
    # move the original to the folder "CHECKME" to be, you know, 
    # checked. 
    #
    if not os.listdir(loc_Orig): 
            os.rmdir(loc_Orig)
    else:
        print ("Could not remove " + loc_Orig + ".")
        print ("Moving to CHECKME directory.")
        if not os.path.isdir(check_Me):
            try:
                os.makedirs(check_Me)
            except:
                print ("Something is wrong. CHECKME couldn't be made.")
                print (loc_Orig + " left in place.")
        try:
            shutil.move(loc_Orig, check_Me)
        except:
            print ("Something is wrong. Couldn't move " + loc_Orig + " under CHECKME.")
            print (loc_Orig + " left in place.")
