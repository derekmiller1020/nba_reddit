import requests
import json
import datetime
import time
from variables import *

class StreamWrapper(object):

    def __init__(self, thread):

        self.thread = thread
        self.credentials = {'user': username, 'passwd': password, 'api_type': 'json', }
        self.headers = {'user-agent': user_agent, }

        self.session_client = requests.session()

        #login
        r = self.session_client.post('http://www.reddit.com/api/login', data=self.credentials, headers=self.headers)
        mod_json = json.loads(r.text)

        #store session modhash
        self.session_client.modhash = mod_json['json']['data']['modhash']

    #recurse function for streaming comments
    def the_post(self):

        #set the create timestamp for cache purposes
        the_redis.set('connect_timestamp', datetime.datetime.now())

        #get the id in the ajax post to populate the url
        url = 'http://www.reddit.com/r/nba/comments/%s/.json?sort=new&limit=50' % self.thread
        get_data = self.session_client.get(url, headers=self.headers)

        #if the status != 200, Reddit probably thinks we are sending too many requests
        if get_data.status_code != 200:
            time.sleep(5)
            return "connection error with reddit"

        else:

            time.sleep(3)
            #Load that data into a dictionary
            dict_it = json.loads(get_data.text)

            #parse through the dictionary and set up a test for redis to check the data
            c = dict_it[1]['data']['children']
            the_test = c[0]['data']['body']

            #If the comment stream has not updated. Start the recursion!
            if the_redis.get('body') == the_test:
                time.sleep(3)
                self.the_post()

            else:
                full_data = []
                #append some stuff
                for item in c:
                    x = item['data']
                    if 'body' in x:

                        full_data.append(
                            {
                                'author': x['author'],
                                'body': x['body'],
                                'ups': x['ups'],
                                'downs': x['downs'],
                                'team': x['author_flair_css_class']
                            }
                        )

                        #Redis, set a new body variable
                        the_redis.set('body', the_test)

                full_json = json.dumps(full_data)

                #congrats request! You made it!
                return full_json