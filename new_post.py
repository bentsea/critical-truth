#!/usr/bin/python3

import requests
import sys, getopt
import json
import re
import time
import os

pathPrefix = "/home/ubuntu/workspace/"
postPath = pathPrefix + "_posts" + time.strftime("/%Y/%m/")
imgPath = pathPrefix + "img" + time.strftime("/%Y/%m/")


if os.path.isdir(postPath) == False:
   os.makedirs(postPath)
if os.path.isdir(imgPath) == False:
   os.makedirs(imgPath)

def slugify(s):
    s = s.lower()
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')
    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')
    return s
    
def genReview(data,userName):
   url="http://www.omdbapi.com/?"
   movieInfo=json.loads(requests.get(url,params=data).text)
   
   try:
      imdbURL = 'http://www.imdb.com/title/' + movieInfo['imdbID']
   except KeyError:
      print(movieInfo['Error'] + ' Please try a different title. Title must be exact match.')
      sys.exit(2)
   
   output = '---'
   output = output + '\ntitle: "' + movieInfo['Title'] + ' (' + movieInfo['Year'] + ')"'
   output = output + '\nblurb: ""'
   output = output + '\nfinal-verdict: ""'
   output = output + '\nrating: '
   output = output + '\ncategories: [reviews, movies, ' + movieInfo['Genre'] + ']'
   output = output + '\ncarousel: https://img.critical-truth.com/img/' + time.strftime("%Y/%m/")
   output = output + '\nauthor: ' + userName
   output = output + '\nreviewInfo:'
   output = output + '\n   name: "' + movieInfo['Title'] + '"'
   output = output + '\n   sameAs: "' + imdbURL + '"'
   output = output + '\n   image: "' + movieInfo['Poster'] + '"'
   output = output + '\n   director: "' + movieInfo['Director'] + '"'
   output = output + '\n   dateCreated: "' + movieInfo['Released'] + '"'
   output = output + '\n---\n\n\n'
   
   
   fileName = time.strftime("%Y-%m-%d-") + slugify(movieInfo['Title'] + ' (' + movieInfo['Year'] + ')') + ".markdown"
   
   makeFile(fileName,output)
   
   
def genEditorial(articleTitle, userName):
   output = '---'
   output = output + '\ntitle: "' + articleTitle + '"'
   output = output + '\nblurb: ""'
   output = output + '\ncategories: [editorials]'
   output = output + '\ncarousel: https://img.critical-truth.com/img/' + time.strftime("%Y/%m/")
   output = output + '\nauthor: ' + userName
   output = output + '\n---\n\n\n'
   fileName = time.strftime("%Y-%m-%d-") + slugify(articleTitle) + ".markdown"
   makeFile(fileName,output)
   
def makeFile(fileName,output):
   file = open(postPath + fileName,"w")
   file.write(output)
   file.close()
   print("Success, new file created: " + fileName)



def main(argv):
   try:
      opts, args = getopt.getopt(argv,"ey:t:u:",["title=","year=","user=","editorial="])
   except getopt.GetoptError:
      print('Usage: python3 new_post.py -t "Movie Title" -u "Author Username" [-y "Release year"]')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ('-u','--user'):
         userName = arg
      elif opt in ("-t", "--title"):
         filmTitle = arg
      elif opt in ("-y", "--year"):
         releaseYear = arg
      elif opt in ("-e","--editorial"):
         editorial = True
      else:
         print('Usage: python3 new_post.py -t "Movie Title" -u "Author Username" [-y "Release year"]')
         sys.exit(2)
   try:
      userName
      if editorial == True:
         genEditorial(filmTitle,userName)
         exit()
      else:
         try:
            data={'t':filmTitle,'y':releaseYear,'r': 'json'}
         except:
            data={'t':filmTitle,'r': 'json'}
         genReview(data,userName)
         exit()
   except Exception as err:
      print(str(err))
      print('Usage: python3 new_post.py -t "Movie Title" -u "Author Username" [-y "Release year"]')
      sys.exit(2)
      
   
      
      


if __name__ == "__main__":
   main(sys.argv[1:])