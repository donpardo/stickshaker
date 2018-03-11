#!/usr/bin/env python
#
# Crudely reorganizes a music collection based on 
# the contents of a file described in the README

# TODOS:
# - Define appropriate variables in an external file
# - check that glbl_musicRoot exists and is a directory
# - check that glbl_moveFileName exists. if not, allow user to select file interactively
# - check that all folders on left in glbl_moveFileName file exist. if not, abort.
# - allow wildcards on left side of moves (example: Bob Dylan*:::Bob Dylan/)
# - final pass to clean up directory names regardless of whether or not
#       they are in the moves file.
# - allow user to review, edit and supplement the my_style entries
# - create dry run similar to rsync
# - detect filesystem on musicRoot. If not a case sensitive filesystem, do something
#       about moving files from "DiReCtoRY" to "Directory"
# - all users to set their own musicRoot, moveFileName, failDir and checkDir
# - report number of files moved, directories deleted, etc.
# - better logging in general

import sys
import os
import re # regular expressions
import shutil
#import logging

# glbl_ = global
# fxx_ = function XX
#

glbl_musicRoot = '/Users/matt/Stickshaker/music_test/music_dirs'
glbl_dataRoot = '/Users/matt/Stickshaker/data'
#glbl_dataRoot = '/nethome/mhanes/Personal/Stickshaker/data'
#glbl_musicRoot = '/nethome/mhanes/Personal/Stickshaker/music_test/music_dirs'
glbl_moveFileName = 'moves'
#glbl_moveFileName = 'linda_moves'
glbl_moveFilePath = os.path.join(glbl_dataRoot,glbl_moveFileName)
glbl_failDir = os.path.join(glbl_musicRoot,"EXCEPTIONS")
glbl_checkDir = os.path.join(glbl_musicRoot,"CHECKME")
glbl_myFolders = dict()
glbl_myBadDirs = list()

def func_SetStyle(fss_chngLoc):
    print("SetStyle successfully called.")
    # fss_styleChange should be put in a file later so it can be 
    # configured by the user
    fss_styleChange = { " the ":" The ", " and ":" and ", " & ":" and ", "_":" ", " w ":" with ", "  ":" " }
    print("func_SetStyle successfully called")
    # This function cleans up and standardizes the name of the 
    # destination folder (loc_Dest), using the values set in 
    # fss_styleChange above.
    for fss_target in fss_styleChange:
        fss_replacement = re.compile(re.escape(fss_target), re.IGNORECASE)
        fss_chngLoc = fss_replacement.sub(fss_styleChange[fss_target], fss_chngLoc)
        fss_chngLoc = re.sub(' +', ' ', fss_chngLoc)
    return fss_chngLoc

def func_MoveTest(fmt_From, fmt_To):
    # fmt_From = file or directory being tested
    # fmt_To = Destination directory
    # fmt_locOG = original location before style adjustments
    print("func_MoveTest successfully called.")
    print("From: " + fmt_From + "\nTo: " + fmt_To)
    print ("-------------")
    #
    # Test each of the contents of fmt_From to see if it is a
    # directory. If it is, create it in the destination then move down
    # one level and do it again. If it is a file, move it.
    #
    fmt_Files = os.listdir(fmt_From)
    for fmt_MF in fmt_Files:
        fmt_testPath = os.path.join(fmt_From, fmt_MF)
        fmt_finalDest = os.path.join(fmt_To, fmt_MF)
        # if fmt_testPath is a file, move it.
        if os.path.isfile(fmt_testPath):
            func_MoveFiles(fmt_testPath, fmt_finalDest, glbl_failDir)
        # if fmt_testPath is a directory, make it, then re-call func_MoveTest
        # giving fmt_testPath as fmt_From
        if os.path.isdir(fmt_testPath):
            fmt_NewTo = os.path.join(fmt_To, fmt_MF)
            try:
                print ("Making dir: " + fmt_NewTo)
                os.mkdir(fmt_NewTo)
            except (OSError):
                pass
            func_MoveTest(fmt_testPath, fmt_NewTo)
    return

def func_MoveFiles(fmf_filePath, fmf_finalLoc, fmf_failDir):
    # fmf_fileName = path and name of file being moved
    # fmf_finalLoc = destination
    # fmf_failDir = location for files that can't be moved
    print("MoveFiles successfully called")
    print ("fmf_filePath = " + fmf_filePath)
    print ("fmf_finalLoc = " + fmf_finalLoc)
    try:
        shutil.move(fmf_filePath, fmf_finalLoc)
    # This needs fixing:
    except (IOError):
        print (IOError)
        raise
        pass
    return

# deletes empty directories from the bottom up. Stolen from
# https://unix.stackexchange.com/questions/396763/recursively-cleanup-all-folders-and-sub-folders-in-a-folder-that-have-no-files-i
# I am not proud.

def func_DeleteDirs(fdd_topLevel):
    fdd_deleteCount == 0
    for fdd_root, fdd_dirs, fdd_files in os.walk(fdd_topLevel, topdown=False):
        for fdd_name in fdd_dirs:
            fdd_dirPath = os.path.join(fdd_root, fdd_name)
            if not os.listdir(fdd_dirPath):  # An empty list is False
                os.rmdir(os.path.join(fdd_root, fdd_name))
                fdd_deleteCount += 1
    print (fdd_deleteCount + "empty directories deleted.")
    return

# actual thing that does stuff follows.

with open(glbl_moveFilePath, "r") as main_MoveLine:
    for main_Line in main_MoveLine:
        #
        # get the two locations
        #
        main_locOrig, main_locDest = main_Line.split(":::")
        main_locOrig = main_locOrig.rstrip()
        main_locDest = main_locDest.rstrip()
        #
        # get the last character of the destination
        #
        main_LastChar = main_locDest[-1:]
        #
        # If the destination has a trailing slash, the original
        # directory gets put under the destination
        #
        if main_LastChar == '/':
            main_locDest = os.path.join(main_locDest,main_locOrig)
        #
        # set the destination per style
        #
        main_locDest = func_SetStyle(main_locDest)
        #
        # build destination directory full path
        #
        main_locDest = os.path.join(glbl_musicRoot,main_locDest)
        main_locOrig = os.path.join(glbl_musicRoot,main_locOrig)
        print('Moving: "' + main_locOrig + '"\n    to: "' + main_locDest +'"')
        #
        # add to dictionary for use below
        #
        glbl_myFolders[main_locOrig] = main_locDest
        #
        # check if left side exists. note it if it does not.
        #
        if not os.path.isdir(main_locOrig):
            glbl_myBadDirs.append(main_locOrig)
#
# alert the user, if needed
#
if glbl_myBadDirs:
    print ("The following directories do not exist. You need to fix this before proceeding.")
    for my_Dir in glbl_myBadDirs:
        print (my_Dir)
        # consider adding this back. If a directory is empty, it gets deleted at the end.
        # os.makedirs(my_Dir)
    sys.exit(254)
#
# Time to do the actual moves:
#
for main_locOrig in glbl_myFolders:
    main_locDest = glbl_myFolders[main_locOrig]
    #
    # Make the destination directory 
    #
    if not  os.path.isdir(main_locDest):
       print ("Making directory " + main_locDest)
       os.makedirs(main_locDest)
    #
    # Move the files from the original to the destination
    #
    main_locDest = main_locDest + "/"
    main_locOrig = main_locOrig + "/"
    print ("Moving")
    print ("    ORIG: " + main_locOrig)
    print ("    DEST: " + main_locDest)
    print ("-------------")
    func_MoveTest(main_locOrig,main_locDest)
print("Moves finished. ")

#
# Finally, delete all the empty directories
#
print ("Deleting empty directories. Hold please.")
func_DeleteDirs(glbl_musicRoot)

print("Finished. Hope this helped.")