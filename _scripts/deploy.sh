#!/bin/bash

if  [[ $TRAVIS_PULL_REQUEST = "false" ]]
then
    lftp -u ${USER},${PASS} ${HOST} <<EOF
    set ftp:ssl-allow false
    rm -r ./public_html
    mkdir public_html
    bye
EOF
    cd _site || exit
    lftp -u ${USER},${PASS} ${HOST} <<EOF
    set ftp:ssl-allow false
    mirror -R --parallel -c . ./public_html
    bye
EOF
fi