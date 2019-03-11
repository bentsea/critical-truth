#!/bin/bash

if  [[ $TRAVIS_PULL_REQUEST = "false" ]]
then
    lftp -u $USERNAME,$PASSWORD sftp://$HOST<<EOF
    rm -r public_html
    mkdir public_html
    mirror -R --parallel -c _site/ ./public_html
    bye
EOF
fi