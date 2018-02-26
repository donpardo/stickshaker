#!/bin/bash
MUSIC_HOME="/Users/matt/Stickshaker/music_test/music_dirs/"
while IFS='' read -r line || [[ -n "$line" ]]; do
    mkdir -p  "${MUSIC_HOME}${line}"
    file=`openssl rand -hex 4`
    touch "${MUSIC_HOME}/${line}/${file}.mp3"
done < "$1"
