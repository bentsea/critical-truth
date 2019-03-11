#!/usr/bin/python3

import requests
import sys, getopt
import json
import re
import time
import os
from PIL import Image
from io import BytesIO
from resizeimage import resizeimage

pathPrefix="/workspace/critical-truth/app/"
apiKey="6cd4598528ca8c2817528493556b2d49"
language="en-US"
url="https://api.themoviedb.org/3/"
multiSearch = "search/multi"

postPath=pathPrefix + "_posts" + time.strftime("/%Y/%m/")
imgPath=pathPrefix + "img" + time.strftime("/%Y/%m/")

max_width = 1920


if os.path.isdir(postPath) == False:
   os.makedirs(postPath)
if os.path.isdir(imgPath) == False:
   os.makedirs(imgPath)
   
def generateSession():
   readAccessToken="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Y2Q0NTk4NTI4Y2E4YzI4MTc1Mjg0OTM1NTZiMmQ0OSIsInN1YiI6IjU5MjEwMzhmYzNhMzY4N2E2NDA1MDEwZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.A2sLjkzHDwJz5luDyRp9To_0beIxkPtIJJs_sUQCRSA"
   validate1="bentsea"
   validate2="k1Doq8NCz7HEaw3"
   payload={'api_key':apiKey}
   payload['request_token']=json.loads(requests.get(url+'authentication/token/new',data=payload).text)['request_token']
   payload['username']=validate1
   payload['password']=validate2
   requests.get(url+'authentication/token/validate_with_login',data=payload)
   return json.loads(requests.get(url+'authentication/session/new',data=payload).text)
   
def saveImage(imgURL,imgName):
   response = requests.get(imgURL)
   img = Image.open(BytesIO(response.content))
   new_height = int(img.height * (max_width / img.width))
   img = img.resize((max_width,new_height))
   img = resizeimage.resize_crop(img,[1920,900])
   img.save(imgPath + imgName,optimize=True,quality=60)

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
    
def genReview(data,userName, releaseYear=""):
   searchData=json.loads(requests.get(url+multiSearch,data=data).text)['results']
   
   try:
      searchData[0]
   except KeyError:
      print('No results found for tile query.')
      sys.exit(2)
      
   for i in searchData:
      if i['media_type'].find('movie') != -1:
         if i['release_date'].find(releaseYear) != -1:
            auth={'api_key':apiKey}
            movieInfo = json.loads(requests.get(url+i['media_type'] + '/' + str(i['id']), data=auth).text)
            credits = credits=json.loads(requests.get(url+i['media_type'] + '/' + str(i['id']) + '/credits',data=auth).text)
            break
   
   imdbURL = 'http://www.imdb.com/title/' + movieInfo['imdb_id']
   slug=slugify(movieInfo['title'])
   imgName = slug + '-cover.jpg'
   saveImage('https://image.tmdb.org/t/p/original'+movieInfo['backdrop_path'],imgName)
      
   
   output = '---'
   output = output + '\ntitle: "' + movieInfo['title'] + ' (' + movieInfo['release_date'].split('-')[0] + ')"'
   output = output + '\nblurb: ""'
   output = output + '\ncategories: [review,movie,' + ','.join([d['name'] for d in movieInfo['genres']]) + ']'
   output = output + '\nimage: https://img.critical-truth.com/img' + time.strftime("/%Y/%m/") + imgName
   #output = output + '\nbanner: https://img.critical-truth.com/img/' + time.strftime("%Y/%m/")
   output = output + '\nauthor: ' + userName
   output = output + '\nreviewInfo:'
   output = output + '\n   final-verdict: ""'
   output = output + '\n   rating: '
   output = output + '\nsubjectInfo:'
   output = output + '\n   type: Movie'
   output = output + '\n   name: "' + movieInfo['title'] + '"'
   output = output + '\n   sameAs: "' + imdbURL + '"'
   output = output + '\n   image: "https://image.tmdb.org/t/p/original' + movieInfo['poster_path'] + '"'
   output = output + '\n   director: "' + next(item for item in credits['crew'] if item["job"] == "Director")['name'] + '"'
   output = output + '\n   dateCreated: "' + movieInfo['release_date'] + '"'
   output = output + '\npublished: False'
   output = output + '\n---\n\n\n'
   
   
   fileName = time.strftime("%Y-%m-%d-") + slug + ".markdown"
   
   makeFile(fileName,output)
   
def genGameReview(title,userName,releaseYear=""):
   slug=slugify(title)
   
   output = '---'
   output = output + '\ntitle: "' + title + ')"'
   output = output + '\nblurb: ""'
   output = output + '\ncategories: [review,videogame]'
   output = output + '\nimage: https://img.critical-truth.com/img' + time.strftime("/%Y/%m/")
   #output = output + '\nbanner: https://img.critical-truth.com/img/' + time.strftime("%Y/%m/")
   output = output + '\nauthor: ' + userName
   output = output + '\nreviewInfo:'
   output = output + '\n   final-verdict: ""'
   output = output + '\n   rating: '
   output = output + '\nsubjectInfo:'
   output = output + '\n   type: VideoGame'
   output = output + '\n   name: ""'
   output = output + '\n   operatingSystem: ""'
   output = output + '\n   applicationCategory: "Game"'
   output = output + '\n   dateCreated: ""'
   output = output + '\npublished: False'
   output = output + '\n---\n\n\n'
   
   
   fileName = time.strftime("%Y-%m-%d-") + slug + ".markdown"
   
   makeFile(fileName,output)
   
def genBookReview(title,userName,releaseYear=""):
   slug=slugify(title)
   
   output = '---'
   output = output + '\ntitle: "' + title + ')"'
   output = output + '\nblurb: ""'
   output = output + '\ncategories: [review,book]'
   output = output + '\nimage: https://img.critical-truth.com/img' + time.strftime("/%Y/%m/")
   output = output + '\nauthor: ' + userName
   output = output + '\nreviewInfo:'
   output = output + '\n   final-verdict: ""'
   output = output + '\n   rating: '
   output = output + '\nsubjectInfo:'
   output = output + '\n   type: Book'
   output = output + '\n   name: ""'
   output = output + '\n   sameAs: ""'
   output = output + '\n   image: ""'
   output = output + '\n   author: ""'
   output = output + '\n   author: ""'
   output = output + '\n   dateCreated: ""'
   output = output + '\npublished: False'
   output = output + '\n---\n\n\n'
   
   
   fileName = time.strftime("%Y-%m-%d-") + slug + ".markdown"
   
   makeFile(fileName,output)
   
   
def genEditorial(articleTitle, userName):
   output = '---'
   output = output + '\ntitle: "' + articleTitle + '"'
   output = output + '\nblurb: ""'
   output = output + '\ncategories: [editorial]'
   output = output + '\nimage: https://img.critical-truth.com/img/' + time.strftime("%Y/%m/")
   output = output + '\nauthor: ' + userName
   output = output + '\npublished: False'
   output = output + '\n---\n\n\n'
   fileName = time.strftime("%Y-%m-%d-") + slugify(articleTitle) + ".markdown"
   makeFile(fileName,output)
   
def makeFile(fileName,output):
#Create a file using the filename and postpath arguments and populate it with the output.
   with open(postPath + fileName,"w",encoding='utf-8') as file:
      file.write(output)
   print("Success, new file created: " + fileName)



def main(argv):
#Get options from command line.
   editorial=False
   releaseYear=''
   media='movie'
   try:
      opts, args = getopt.getopt(argv,"em:y:t:u:",["title=","year=","user=","editorial=","media="])
   except getopt.GetoptError:
      print('Usage: python3 new_post.py -t "Movie Title" -u "Author Username" [-y "Release year"]')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ('-u','--user'):
         userName = arg
      elif opt in ("-t", "--title"):
         title = arg
      elif opt in ("-y", "--year"):
         releaseYear = arg
      elif opt in ("-e","--editorial"):
         editorial = True
      elif opt in ("-m","--media"):
         media = arg.lower()
      else:
         print('Boo Usage: python3 new_post.py -t "Movie Title" -u "Author Username" [-y "Release year"]')
         sys.exit(2)
         
#Assign a username if one wasn't set.
   try:
      userName
   except:
      userName="dscott"
     
#Generate the post.
   try:
      if editorial == True:
         genEditorial(title,userName)
         exit()
      elif media=='movie':
         data={'api_key':apiKey,'query':title,'language':language}
         genReview(data,userName,releaseYear)
         exit()
      elif media=='game':
         genGameReview(title,userName,releaseYear)
         exit()
      elif media=='book':
         genBookReview(title,userName,releaseYear)
         exit()
      else:
         exit()

         
#Let the user know they fucked up if they fucked up.
   except Exception as err:
      print(str(err))
      print('Usage: python3 new_post.py -t "Movie Title" -u "Author Username" [-y "Release year"]')
      sys.exit(2)
      
   
      
      


if __name__ == "__main__":
   main(sys.argv[1:])