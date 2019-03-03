#!/bin/bash

if  [[ $TRAVIS_PULL_REQUEST = "false" ]]
then
    ncftp -u "$USER" -p "$PASS" "$HOST"<<EOF
    rm -rf ./public_html/*
    quit
EOF

    cd _site || exit
    ncftpput -R -v -u "$USER" -p "$PASS" "$HOST" ./public_html .
fi