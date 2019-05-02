#!/usr/bin/python3

import requests
import random
import sys, getopt
import json
import re
import time
import os
from PIL import Image
from io import BytesIO
from resizeimage import resizeimage
from jinja2 import FileSystemLoader, Environment
from pathlib import Path

pathPrefix="/workspace/eskimotv"
appPrefix="/app"
apiKey="6cd4598528ca8c2817528493556b2d49"
language="en-US"
url="https://api.themoviedb.org/3/"
multiSearch = "search/multi"
dateSuffix = time.strftime("/%Y/%m/")
postSuffix = "/_posts" + dateSuffix
imgSuffix = "/img" + dateSuffix

postPath=pathPrefix + appPrefix + postSuffix
imgPath=pathPrefix + appPrefix + imgSuffix

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
   return imgSuffix + imgName

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
    
def filename(name):
   file = Path(postPath+name)
   if file.is_file():
      option = ""
      while(option not in ['o','g','c']):
         option = input("{} already exists. [o]verwrite,[g]enerate as parralel article, or [c]ancel? ".format(name))
      if option == 'o':
         return name
      elif option == 'g':
         file_chunks = name.split('.')
         if len(file_chunks) == 2:
            return filename("{}.{}.{}".format(file_chunks[0],"alternate",file_chunks[1]))
         elif len(file_chunks) > 2:
            extension = file_chunks.pop(-1)
            return filename("{}.{}.{}".format(".".join(file_chunks),"alternate",extension))
      else:
         print("Exiting without saving.")
         exit()
   else:
      return name
    
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
            movieInfo['type']=i['media_type']
            movieInfo['release_year'] = movieInfo['release_date'].split('-')[0]
            credits = credits=json.loads(requests.get(url+i['media_type'] + '/' + str(i['id']) + '/credits',data=auth).text)
            movieInfo['director'] = next(item for item in credits['crew'] if item["job"] == "Director")['name']
            movieInfo['categories'] = [d['name'] for d in movieInfo['genres']]
            movieInfo['images'] = json.loads(requests.get("{}{}/{}/images".format(url,i['media_type'],i['id']), data=auth).text)   
            movieInfo['imdb_url'] = "http://www.imdb.com/title/{}".format(movieInfo['imdb_id'])
            movieInfo['slug'] = slugify(movieInfo['title'])
            fileName = filename("{}{}.markdown".format(time.strftime("%Y-%m-%d-"),movieInfo['slug']))
            imageIndex = random.randint(0,len(movieInfo['images']['backdrops'])-1)
            movieInfo['cover_image'] = saveImage('https://image.tmdb.org/t/p/original{}'.format(movieInfo['images']['backdrops'][imageIndex]['file_path']),"{}-{}-cover.jpg".format(movieInfo['slug'],imageIndex))
            break
      
   templateLoader = FileSystemLoader("{}/scripts/templates".format(pathPrefix))
   env = Environment(loader=templateLoader)
   template = env.get_template('article.markdown')
   output = template.render(author_username=userName,subjectItem=movieInfo,review=True)
   
   
   makeFile(fileName,output)
   
   
def genEditorial(articleTitle, userName):
      
   templateLoader = FileSystemLoader("{}/scripts/templates".format(pathPrefix))
   env = Environment(loader=templateLoader)
   template = env.get_template('article.markdown')
   output = template.render(title=articleTitle,author_username=userName)
   

   fileName = filename("{}{}.markdown".format(time.strftime("%Y-%m-%d-"),slugify(articleTitle)))
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
         print('Boo Usage: new -t "Movie Title" -u "Author Username" [-y "Release year"]')
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
      else:
         exit()

         
#Let the user know they fucked up if they fucked up.
   except Exception as err:
      print(str(err))
      print('Usage: new -t "Movie Title" -u "Author Username" [-y "Release year"]')
      sys.exit(2)
      
   
      
      


if __name__ == "__main__":
   main(sys.argv[1:])