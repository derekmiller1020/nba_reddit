import requests
import json
import datetime
import time
from variables import *

class the_long_poll(object):

    def __init__(self, thread):
        self.thread = thread
        time.sleep(1)

    def the_post(self):

        #use this datetime to disregard reddit cache
        the_date = datetime.datetime.now()

        #get the id in the ajax post to populate the url
        url = 'http://www.reddit.com/r/nba/comments/%s/.json?%s&sort=new' % (self.thread, the_date)
        get_data = requests.get(url)

        if get_data.status_code != 200:
            time.sleep(3)
            self.the_post()

        dict_it = json.loads(get_data.text)

        #parse through the dictionary
        c = dict_it[1]['data']['children']
        full_data = []
        the_test = c[0]['data']['body']

        if the_redis.get('body') == the_test:
            time.sleep(6)
            self.the_post()

        else:
            for item in c:
                x = item['data']
                if 'body' in x:

                    full_data.append(
                        {
                            'author': x['author'],
                            'body': x['body'],
                            'ups': x['ups'],
                            'downs': x['downs']
                        }
                    )

                    the_redis.set('body', the_test)

            full_json = json.dumps(full_data)

            return full_json