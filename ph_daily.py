# coding=utf-8
import requests
import json
import re
import schedule
import time
import telegram
import bmemcached
import os
from dotenv import load_dotenv
load_dotenv()

MIN_VOTE = 100

# telegram bot
token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
bot = telegram.Bot(token=token)

# memcachier
servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')
mc = bmemcached.Client(servers, username=user, password=passw)
mc.enable_retry_delay(True)  # Enabled by default. Sets retry delay to 5s.

#product hunt
developer_token = os.environ.get('PH_TOKEN', '')

def fetch_posts():
    url = 'https://api.producthunt.com/v2/api/graphql'
    headers = {'Authorization': 'Bearer {}'.format(developer_token)}
    data = {'query':'{\n  posts(first: 5) {\n    edges {\n      node {\n        id\n        name\n        description\n        url\n        votesCount\n    \t\ttopics {\n    \t\t  edges {\n    \t\t    node {\n              name\n    \t\t    }\n    \t\t  }\n    \t\t}\n      }\n    }\n  }\n}\n'}
    try:
        r = requests.post(url, json = data, headers=headers)
        result = r.json()
        if result is not None:
            print(result)
            for item in result['data']['posts']['edges']:
                node = item['node']
                if node['votesCount'] > MIN_VOTE:
                    topics = list(map(lambda x: re.sub('[\s+]', '', x['node']['name']), node['topics']['edges']))
                    topicStr = ' #'.join(topics)
                    send_to_telegram(node['id'], node['name'], node['description'], node['url'], topicStr)
    except:
        print('Someting went wrong while fetching posts!')

def send_to_telegram(id, title, description, link, topics):
    if mc.get(id):
        print(u'"{}" already posted, ignore!'.format(title))
    else:
        text = u'''
*{}*\t[👉🔗👈]({})
{}
#{}
        '''.format(title, link, description, topics)
        print(u'Posting "{}"'.format(title))
        bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
        mc.set(id, True)

def main():
    fetch_posts()

if __name__ == "__main__":
    main()
    schedule.every(10).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)