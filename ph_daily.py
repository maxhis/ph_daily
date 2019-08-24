import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import telegram
import bmemcached
import os
import schedule
import time
from dotenv import load_dotenv
load_dotenv()

BASE_URL = 'https://www.producthunt.com'
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


def download_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Cache-Control": "no-cache",
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.text


def get_posts(html):
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    # 每个ul是一天的数据，默认只有当天的
    today = soup.find(name='ul', class_=re.compile('^postsList'))
    for item in today.children:
        votes = item.select_one('button > span > span').get_text()
        topic_tag = item.find(name='a', class_=re.compile('^postTopicLink'))
        if topic_tag is not None and int(votes) >= MIN_VOTE:
            link = urllib.parse.urljoin(BASE_URL, item.find('a').get('href'))
            title = item.find('h3').get_text()
            description = item.find('p').get_text()
            topic = topic_tag.find('span').get_text()
            print('title: {} desc: {} lnik: {} votes:{} topic:{}\n'.format(
                title, description, link, votes, topic))
            send_to_telegram(title, description, link, votes, topic)


def send_to_telegram(title, description, link, votes, topic):
    key = link.split('/')[-1]
    if mc.get(key):
        print('{} already posted, ignore!'.format(title))
    else:
        text = '''
*{}*\t[👉🔗👈]({})
{}
#{}
        '''.format(title, link, description, re.sub('[\s+]', '', topic))
        bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
        mc.set(key, True)


def main():
    html = download_page(BASE_URL)
    get_posts(html)


if __name__ == "__main__":
    schedule.every(10).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
