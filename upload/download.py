import os, glob
import youtube_dl
from api import getPosts

video_list = []

class Video:
    def __init__(self, subreddit, range):
        split_list = []
        self.subreddit = subreddit
        for i in range:
            print(i)
            # print(getPosts(self.subreddit, i))
            try:
                parse = getPosts(subreddit, i)[i-1]['secure_media']['oembed']['html']
                video_list.append(getPosts(subreddit, i)[i-1]['secure_media']['oembed']['title'] + "mp4")
                split_list = parse.split(" ")
                split_list = split_list[3].split('"')
                split_list = split_list[1].split("?")
                url = split_list[0]
                print(url)
                # url_object = URL(url, i ,getPosts(subreddit, i)[i-1]['secure_media']['oembed']['title'] + ".mp4")
            except:
                print("EXCEPTION IN INIT")
                url = getPosts(self.subreddit, i)[i-1]['url']
                print(getPosts(self.subreddit,i)[i-1]['title'])
                video_list.append(getPosts(self.subreddit,i)[i-1]['title']+ ".mp4")
                print(url)
            download_video(url)

            #video_list.append(url_object)

    # def __init__():
    #     print("initialized")


    def get_video_list(self):
        return video_list
        # del video_list[:]
    def download_more_videos(self, range):
        for i in range:
            print(i)
            # print(getPosts(self.subreddit, i))
            try:
                parse = getPosts(subreddit, i)[i-1]['secure_media']['oembed']['html']
                video_list.append(getPosts(subreddit, i)[i-1]['secure_media']['oembed']['title'] + "mp4")
                split_list = parse.split(" ")
                split_list = split_list[3].split('"')
                split_list = split_list[1].split("?")
                url = split_list[0]
                print(url)
                # url_object = URL(url, i ,getPosts(subreddit, i)[i-1]['secure_media']['oembed']['title'] + ".mp4")
            except:
                print("EXCEPTION IN DOWNLOAD_MORE_VIDEOS")
                url = getPosts(self.subreddit, i)[i-1]['url']
                print(getPosts(self.subreddit,i)[i-1]['title'])
                video_list.append(getPosts(self.subreddit,i)[i-1]['title']+ ".mp4")
                print(url)
            download_video(url)

    def clear_video_library(self, currentVideoTitles):
        cwd = os.getcwd()
        print(cwd)
        for title in currentVideoTitles:
            for item in os.listdir(cwd + "\Videos"):
                if item in title:
                    print("skip")
                else:
                    os.remove(os.path.join(cwd + "\Videos",item))
                    print("Removed: " +item)

class URL:
    def __init__(self, url, postIndex, title):
        self.url = url
        self.postIndex = postIndex
        self.title = title


def download_video(url):
    ydl_opts ={
        'verbose': True,
        'format': 'mp4',
        'outtmpl': 'Videos\%(title)s.%(ext)s',
        'noplaylist': True,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("Sucess")
    except:
        print("INVALID URL")

def get_next_list(currentIndex, futureIndex):
    this_list = Video.get_video_list()
    next_list = []
    for obj in this_list:
        if obj.postIndex >= currentIndex and currentIndex <= futureIndex:
            next_list.append(obj)
    print(this_list)
    return(next_list)
    # del video_list[:]
def clear_video_library(currentVideoTitles):
    cwd = os.getcwd()
    print(cwd)
    for title in currentVideoTitles:
        for item in os.listdir(cwd + "\Videos"):
            if item in title:
                print("skip")
            else:
                os.remove(os.path.join(cwd + "\Videos",item))
                print("Removed: " +item)

        # os.remove(itemsInDir)

        # print("THIS DAT ITEM BOY" + itemsInDir)
        # if itemsInDir != currentVideoTitle:
        #     os.remove(itemsInDir)
            # if os.path.isdir(os.path.join(cwd +"\Videos", itemsInDir)):
            #     functToDeleteItems(os.path.isdir(os.path.join(cwd +"\Videos", itemsInDir)))
            # else:
            #     os.remove(os.path.join(cwd + "\Videos",itemsInDir))



# def get_video():
# download_video("https://www.liveleak.com/view?t=aI6In_1522389432")
# videos = Video("Videos", range(1,2))
# videos.download_more_videos(range(2,3))
# Video("Videos", range(2,3))

# print(Video.get_video_list())
# test_list = Video.get_video_list()
# test_list2 = get_next_list(2,3)
# # test_list.append(Video.get_video_list())
# print(test_list)
# for test_obj in test_list:
#     print(test_obj.postIndex)
#     print(test_obj.url)
#     print(test_obj.title)
# print(get_next_list(1,1))
# for obj in test_list2:
#     print(test_obj.postIndex)
#     print(test_obj.url)
#     print(test_obj.title)
#     title = test_obj.title
# clear_video_library(title)


##update buffer()
#     This function will update everytime the user clicks next on the video
#     It will load 1 more video and delete the oldest video
#         the oldest video is the video before the current video the user is watching
#     if videos left is less than 8 the load up the buffer with more videos.
# ##load buffer()
    # The buffer wills tart with 4 videos.
