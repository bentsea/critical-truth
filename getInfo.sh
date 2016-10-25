#!/bin/bash
num='[0-9]'
if [[ $1 =~ ^tt[0-9]+ ]]; then
curl -o movieText.txt "http://www.omdbapi.com/?i=${1}&plot=short&r=json"
else
curl -o movieText.txt "http://www.omdbapi.com/?t=${1}&y=&plot=short&r=json"
fi

 sed 's/","/\n/g' movieText.txt|sed -e 's/":"/: /g' -e 's/{"//g' -e 's/\\"//g'|grep -v -e "Plot: " -e "Poster: " -e "Response: " -e "^imdb" -e "Type: "
