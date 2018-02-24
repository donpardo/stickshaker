#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    mkdir -p  "${line}"
    file=`openssl rand -hex 4`
    touch "${line}/${file}.mp3"
done < "$1"
