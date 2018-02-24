This folder contains a previous attempt using bash.

Because it's what I sort of knew, that's why.

Hey! I came to the realization that it would be easier in python. Don't judge me.

Anyway:

README.txt - this file
finder.sh 
moveit.sh - old non-working attempt at this.
toucher.sh - this one may be useful. it will create a test 
	folder structure from a list of albums. File is in
	the format:
		Artist Name/Album Name
	If you have an existing set of music, you can generate 
	this file with the following:
		find /path/to/music/root -type d -exec echo {} >> ~/data_folder/albums_only
	The script also puts a uniquely named mock mp3 file inside every album.
