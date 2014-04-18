import praw
import redis

r = praw.Reddit(user_agent='r_nba_live_stream')

#login credentials
username = "bobdammit"
password = "guitar3"
user_agent = '/u/bobdammit r/nba comment stream'

SECRET_ID = "eTVKBVaVpiq8_FOQiOY90pSKaj0"
REDIRECT_URI = "http://127.0.0.1:8000/redirect_url"
CLIENT_ID = "NsDFHioWXp9WgA"

the_redis = redis.Redis('localhost')

