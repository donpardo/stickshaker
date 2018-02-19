# stickshaker
script for organizing a music library

This script organizes a music collection based on a file describing the
changes desired. There will be a companion script to generate a set of
test folders for the purposes of dry runs. Eventually there will be a
script to generate a first pass at organizing the folders.

Assumption:
- The folder structure is generally:
    Artist0/Album0
    Artist0/Album1
    Artist1/Album0
    Artist2/Album0

The structure of the changes file is as follows:
- Two fields separated by the string :::
- The leftmost field is the original directory.
- The rightmost field is the desired destination.
- If the destination folder doesn't exist, it is created.
- If the destination field ends in a '/' the original folder will be
moved under the destination folder.
- If the destination field ends in anything else, the contents of the
original folder will be put under the destination.
- At the end of the run, all empty directories are deleted.
- The script also performs the following substitutions on all folders
in the file:
    - '&' becomes 'and'
    - capitalization standardizations unless the words are at the
    beginning of a directory name: and, with, The
    - there may be a flag to skip this in the future.

How I construct *my* file:
- "The" artists are listed without the "The" in front, ie "Beatles"
not "The Beatles". The only exception to this is "The The". See the
example below.

The directories are:
Beatles, The/
    Meet The Beatles/
    Revolver/
Rubber Soul/
The Beatles/
    Beatles For Sale/

The pertinent lines are:
The Beatles:::Beatles
Rubber Soul:::Beatles/

Based on the first line, "Beatles" is created and then the contents of
"The Beatles" will be placed under "Beatles", resulting in:
Beatles/
    Beatles For Sale/
    Meet the Beatles/
    Revolver/
Beatles, The/
Rubber Soul/
The Beatles/

The next line puts the folder "Rubber Soul" under "Beatles"
Beatles/
    Beatles For Sale/
    Meet The Beatles/
    Revolver/
    Rubber Soul/
Beatles, The/
The Beatles/

Then the empty directories are deleted, resulting in:
Beatles/
    Beatles For Sale/
    Meet The Beatles/
    Revolver/
    Rubber Soul/

- Sometimes I want artists listed under artists. Ella Fitzgerald recorded
with various notable ensembles, but she's the featured artist, so this
is the desired end result for me:

Ella Fitzgerald/
    Ella Fitzgerald and Count Basie/
        A Perfect Match
    Ella Fitzgerald and Duke Ellington/
        Ella Fitzgerald Sings The Duke Ellington Songbook
        Ella at Duke's Place
        Ella and Duke at The Cote D'Azur
    Lullabies of Birdland
    Ella Sings Gershwin

This is accomplished by the following lines:
Fitzgerald, Ella:::Ella Fitzgerald
Ella Fitzgerald and Duke Ellington:::Ella Fitzgerald/
Ella Fitzgerald and Count Basie:::Ella Fitzgerald/

Note that in this instance, the capitalization rules used in the script
may produce incorrect album names. I am willing to accept this.

Other items of interest:
- The contents of identically named albums may be merged.
- Links and aliases are not followed or moved.
