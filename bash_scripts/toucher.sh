#!/bin/bash
#MUSIC_HOME="/Users/matt/Stickshaker/music_test/music_dirs/"
MUSIC_HOME="/nethome/mhanes/Personal/Stickshaker/music_test/music_dirs/"
echo "deleting"
rm -rf $MUSIC_HOME/*
echo "creating"
while IFS='' read -r line || [[ -n "$line" ]]; do
    mkdir -p  "${MUSIC_HOME}${line}"
    file=`openssl rand -hex 4`
    touch "${MUSIC_HOME}/${line}/${file}.mp3"
    echo "not empty" >> "${MUSIC_HOME}/${line}/${file}.mp3"
done < "$1"
echo "done."
exit
