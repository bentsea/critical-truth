#!/bin/bash
num='[0-9]'
if [[ $1 =~ ^tt[0-9]+ ]]; then
curl -o movieText.txt "http://www.omdbapi.com/?i=${1}&plot=short&r=json"
else
remSpace="$(echo $1|sed 's/ /+/g')"
curl -o movieText.txt "http://www.omdbapi.com/?t=${remSpace}&y=${2}&plot=short&r=json"
fi

parser="$( sed 's/","/\n/g' movieText.txt|sed -e 's/":"/: /g' -e 's/{"//g' -e 's/\\"//g'|grep -v -e "Plot: " -e "Poster: " -e "Response: " -e "^imdb" -e "Type: ")"
echo -e "--- \n$parser \nauthor: David Scott \nblurb: \nfinal-verdict: \ndate: \nlayout: \ncarousel: \n---"
