#############################################################################
# Author: Kyle Hays
# Date: 5/3/2018
# Abstract: This is a program to create a video library.
#           The library can be made and then updated.
#           The library is self cleaning only keeping the items stated.
#############################################################################


###Dictionary Example########################################################
# The list should contain multiple dictionary items.
# The dictionary should be the id of the video post along with it's url.
# The url can be a link to a gif, video, etc. Any format that youtube_dl has.
# Comment these out when running the program; this code is for testing.
example_dict = [
    {"id": "33",
    "url" : "https://www.youtube.com/watch?v=QlwBjfK6wdk"},
    {"id": "35",
    "url" : "https://www.youtube.com/watch?v=eaW0tYpxyp0"},
    {"id": "36",
    "url" : "https://vimeo.com/131462825"}
]
example2_dict = [
    {"id": "33",
    "url" : "https://www.youtube.com/watch?v=QlwBjfK6wdk"},
    {"id": "35",
    "url" : "https://www.youtube.com/watch?v=eaW0tYpxyp0"}
]
#############################################################################


###Imports###################################################################
import youtube_dl
import os, glob
#############################################################################



###Buffer Object#############################################################
# Buffer object created to keep track and store videos.
# Can create multiple buffer objects, the filenames will be the same as the
# directory passed in creation.
# If the directory is not made it will be automatically generated.
#############################################################################
class Buffer:
####__init__#################################################################
#############################################################################
    def __init__(self, dicter, directory):
        for i in range(0,len(dicter)):
            print(dicter[i]['id'])
            print(dicter[i]['url'])
            url = dicter[i]['url']
            id = dicter[i]['id']
            cwd = os.getcwd()
            directory_new = cwd + directory
            if not os.path.exists(directory_new):
                print("Making new directory: " + directory_new)
                os.makedirs(directory_new)
            else:
                print("Directory exists: " + directory_new)
            self.download_video(url, id)

###download_video############################################################
# This method takes in a url for youtube_dl to download.
# The format will be output as an mp4 and will be saved to a Videos file.
# The title will be the id passed to it.
#
# NOTE: there is an extra space at the beginning of each title to deal with
#       the escappe character in the filename directory causing issues.
#############################################################################
    def download_video(self, url, id):

        ydl_opts ={
            'verbose': True,
            'format': 'mp4',
            'outtmpl': 'Videos\ ' + id +  '.%(ext)s',
            'noplaylist': True,
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print("Download Succesfull")
                print("new file: " + id + ".mp4" )
        except:
            print(url)
            print("INVALID URL")
###clear_library#############################################################
# This is an internal method used to clear items from the directory not listed
# in the list of items passed to this method.
#############################################################################
    def clear_library(self, list):
        items = []
        cwd = os.getcwd()
        print(cwd)
        for item in os.listdir(cwd + "\Videos"):
            print(item)
            items.append(item)
        print("CURRENT DIRECTORY")
        print(items)
        print("CURRENT VIDEO LIST")
        print(list)
        for i in items:
            if i in list:
                print("KEEP: " + i)
            else:
                os.remove(os.path.join(cwd + "\Videos",i))
                print("DELTE: " + i)
###update####################################################################
# This method downlaods all the items in the dictionary passed to it.
# It labels each item with the id from the dictionary.
# The method then calls the internal method to clear the lbrary of items not
# in the dictonary passed for the update.
#
# NOTE: update will only keep the items in the dictonary passed to it;
#       the update method is self cleaning
#############################################################################
    def update(self, dicter):
        list = []
        for i in range(0,len(dicter)):
            print(dicter[i]['id'])
            print(dicter[i]['url'])
            url = dicter[i]['url']
            id = dicter[i]['id']
            list.append(" " + dicter[i]['id'] + ".mp4")
            self.download_video(url, id)
        self.clear_library(list)


###Test of program###########################################################
# Comment these out when running the program; this code is for testing.
buffin = Buffer(example_dict, "\Videos")
buffin.update(example2_dict)
#############################################################################
