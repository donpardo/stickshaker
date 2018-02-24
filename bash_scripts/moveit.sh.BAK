#!/bin/bash
#
# organizes a music collection based on a file containing a list of changes
#
# file format:
# original folder name:::new destination[/]
# If a line ends in a '/' the original folder ahould be put inside the folder 
# on the right side of the ':::' seperator, otherwise the contents of the 
# left side should be moved inside the folder on the right.
# 

MUSICROOT="/Users/matt/music_test/music_dirs/"
LINE=""
OLOC=""
DLOC=""
LEN=9999
DESTDIR=""
ORIGDIR=""
LOGSTMP=`date +%Y%m%d%H%M%S`
LOGDIR="${HOME}/Logs/"
MOVELOG="${LOGDIR}/move-${LOGSTMP}.log"
ERRORLOG="${LOGDIR}/errors-${LOGSTMP}.log"

mkdir -p ${LOGDIR}/OLD
mv -vn ${LOGDIR}/*.log ${LOGDIR}/OLD/
touch ${MOVELOG}
touch ${ERRORLOG}

# Two special directories
mkdir -p "${MUSICROOT}/RM"
mkdir -p "${MUSICROOT}/VARIOUS"

# get rid of the goddamn spaces and the goddamn &'s in filesystem names. 
# and the stupid commas.
# and the parens and the brackets
# adapted from https://stackoverflow.com/questions/21249231/bash-finding-files-with-spaces-and-rename-with-sed
find . -name '* *' -exec bash -c 'DIR=$(dirname "{}" | sed "s/[])([]//g" | sed "s/ /_/g" | sed "s/&/XndX/g" | sed "s/,/cOMMa/g"); \
	BASE=$(basename "{}"); \
	echo mv -v \"$DIR/$BASE\" \"$DIR/$(echo $BASE | sed "s/[])([]//g" | sed "s/ /_/g" | sed "s/&/XndX/g" | sed "s/,/cOMMa/g")\"' \; > ${MUSICROOT}/renamescript.sh 
sh ${MUSICROOT}/renamescript.sh 2>>${ERRORLOG} 1>>${MOVELOG}

# LINE is the line from the file.
# OLOC is the original location
# DLOC is the destination 
while IFS='' read -r LINE || [[ -n "$LINE" ]]; do
	# because we changed spaces to underscores in the filesystem above, we need to match that here. 
	LINE=`echo "$LINE" | sed "s/[[:blank:]]+$//g" | sed "s/,/cOMMa/g" | sed "s/ /_/g" | sed "s/&/XndX/g" | sed "s/[])([]//g"`
	echo "LINE = $LINE" >> ${ERRORLOG}
	# pick the correct side and trim any trailing _'s
    	OLOC=`echo "$LINE" | awk -F":::" {'print $1'} | sed "s/_$//g"`
	echo "OLOC = $OLOC" >> ${ERRORLOG}
    	DLOC=`echo "$LINE" | awk -F":::" {'print $2'} | sed 's/_$//g'`
	echo "DLOC = $DLOC" >> ${ERRORLOG}

	# if $DLOC ends in a '/' then set the destination directory
	# to include the album name
	LEN=$((${#DLOC}-1))
	if [ "${TEST}" = '/' ]; then
		DESTDIR="${DLOC}${OLOC}"
	else
		DESTDIR="${DLOC}"
	fi

	# let's do some neatening, shall we?
	echo "destination = $DEST" >> ${ERRORLOG}
	# if I weren't on Mac I could do case insensitive matching. But I am. So I don't.
	DESTDIR=`echo ${DESTDIR} | sed 's/ & / and /g;s/ And / and /g;s/ With / with /g;s/ the / The /g;s/[[:blank:]]+/ /g'`

	# because DESTDIR, that's why
	ORIGDIR=${OLOC}
	echo "origination = $ORIGDIR" >> ${ERRORLOG}
	echo "destination = $DESTDIR" >> ${ERRORLOG}
	# find all the directories we need under the desitnation and make them:
	for ALBUM in `find ${ORIGDIR} -type d | uniq | awk -F/  '{ $1=""; print}' | sort | uniq | sed 's/^[[:blank:]]*//' | grep [a-zA-Z]`
	do
		echo "mkdir -p ${DESTDIR}/${ALBUM}" >> ${ERRORLOG}
		mkdir -p ${DESTDIR}/${ALBUM} 2>>${ERRORLOG} 1>>${MOVELOG}
		echo "mv -vn ${ORIGDIR}/${ALBUM}/* ${DESTDIR}/${ALBUM}/" >>${ERRORLOG} 
		mv -vn ${ORIGDIR}/${ALBUM}/* ${DESTDIR}/${ALBUM}/ 2>>${ERRORLOG} 1>>${MOVELOG}
		echo "rmdir ${ORIGDIR}/${ALBUM}/" >> ${ERRORLOG}
		rmdir ${ORIGDIR}/${ALBUM}/ 2>>${ERRORLOG} 1>>${MOVELOG}
	done
	# delete the empty dirctories
	echo "deleting empty directories" >> ${ERRORLOG}
	find ${ORIGDIR}  -depth -type d -empty -delete 2>>${ERRORLOG} 1>>${MOVELOG}
done < "$1"

exit 

# and now we put the spaces, etc back in.
echo "un-renaming files and folders." >> ${ERRORLOG} 
find . -name '*_*' -exec bash -c 'DIR=$(dirname "{}" | sed "s/_/ /g" | sed "s/XndX/And/g" | sed "s/cOMMa/,/g"); \
	BASE=$(basename "{}"); \
	echo mv -v \"$DIR/$BASE\" \"$DIR/$(echo $BASE | sed "s/_/ /g" | sed "s/XndX/And/g" | sed "s/cOMMa/,/g")\"' \; > ${MUSICROOT}/emanerscript.sh 
sh ${MUSICROOT}/emanerscript.sh >> ${ERRORLOG}

exit

