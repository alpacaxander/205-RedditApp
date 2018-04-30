from download import Video, URL, download_video, get_next_list, clear_video_library
class VideoBuffer:

    global start
    global end

    def __init__(self, subreddit, range):
        self.subreddit = subreddit
        self.range = range
        self.loadBuffer(subreddit,range)

    def loadBuffer(self, subreddit, range):
        global start
        global end
        this = 0
        thistoo = 0
        self.buffer = Video(subreddit,range)
        print("Buffer loaded: ")
        rangeObj = range
        for i in rangeObj:
            if this == 0:
                this = i
                thistoo=i+1
            else:
                thistoo = i
        start = this
        end = thistoo
        print(start)
        print(end)

    def increaseBuffer(self,range):
        global start
        global end
        this = 0
        thistoo=0
        self.buffer.download_more_videos(range)
        print("increaseing buffer" )
        rangeObj = range
        for i in rangeObj:
            if this == 0:
                this = i
                thistoo=i+1
            else:
                thistoo = i
        start = this
        end = thistoo
        print (start)

    # def defineFullBuff():
    #     end = (start + count) + 1
    #     print("la"+end)

    def buff(self):
        global start
        global end
        this =0
        thistoo = 0
        print("START AND END")
        print( start)
        print(end)
        end = end+2
        rangeObj = range(start,end)
        self.buffer.download_more_videos(rangeObj)
        for i in rangeObj:
            if this == 0:
                this = i
                thistoo=i+1
            else:
                thistoo = i
                print("skipidy do da")
        start = this
        end = thistoo
        print("START AND END UPDATED")
        start = end-1
        print(start)
        print(end)

    def get_video_list(self):
        return(self.buffer.get_video_list())

    def clear_video_library(self, currentVideoTitles, start , finish):
        pass_list= []
        for i in range(start,finish):
            pass_list.append(currentVideoTitles[i])
        self.buffer.clear_video_library(pass_list)
        print(pass_list)



##THIS IS FOR TESTING PURPOSES##
buffer = VideoBuffer("Videos", range(1,2))
#Loads the first video of the buffer object
buffer.increaseBuffer(range(2,3))
#increases the buffers range from 1 video to 2 videos
buffer.buff()
#increases the buffer by 1
#In later versions this will decrease the buffer by 1 as well
buffer.buff()
#current_list = buffer.get_video_list()
#NOT CURRENTLY WORKING
#returns the current_list of videos  you have in your library
print (current_list)

buffer.clear_video_library(current_list, 2, 4)
#clears everything except for the 2nd video in the library
