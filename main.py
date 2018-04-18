import praw, config

reddit = praw.Reddit(client_id=config.id,
                     client_secret=config.secret,
                     password=config.password,
                     user_agent=config.user_agent,
                     username=config.username)

# Create a submission to /r/test
# reddit.subreddit('test').submit('Test Submission', url='https://reddit.com')

# Comment on a known submission
# submission = reddit.submission(url='https://www.reddit.com/comments/5e1az9')
# submission.reply('Super rad!')

# Output score for the first 256 items on the frontpage
# for submission in reddit.front.hot(limit=256):
#     print(submission.score)

sub = input('Subreddit: ')
count = int(input('Count: '))
for post in reddit.subreddit(sub).hot(limit=count):
  print(f'↑{post.score} | {post.title} - {post.author}')
