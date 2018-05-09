import praw
from config import creds

reddit = praw.Reddit(client_id=creds['id'],
                     client_secret=creds['secret'],
                     password=creds['password'],
                     user_agent=creds['user_agent'],
                     username=creds['username'])

# Returns a dictionary containing attributes for the current user
def getUser():
  return reddit.user.me()

# Returns a list of the posts on the user's front page as dictionaries
def getFrontPage(count=None):
  posts = [i.__dict__ for i in list(reddit.front.hot(limit=count))]
  return posts

# Returns a list of the user's subscribed subreddits as dictionaries
def getSubreddits(count=None):
  subs = [i.__dict__ for i in list(reddit.user.subreddits(limit=count))]
  return subs

# Returns a list of the posts from the specified subreddit as dictionaries
def getPosts(sub, count=None): # Add sort parameter?
  posts = [i.__dict__ for i in list(reddit.subreddit(sub).hot(limit=count))]
  return posts

# Submits a text post to the specified subreddit
def submitPost(sub, title, content=''):
  reddit.subreddit(sub).submit(title, selftext=link)

# Submits a link to the specified subreddit
def submitLink(sub, title, link='https://reddit.com'):
  reddit.subreddit(sub).submit(title, url=link)

# Submits a comment on a known post and returns a boolean value indicating whether the comment was posted
def submitComment(postID, comment):
  post = reddit.submission(url='https://www.reddit.com/comments/'+postID)
  try:
    post.reply(comment)
  except Exception as e:
    pass
    return False
  return True
