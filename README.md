# Telegram bot for Product Hunt Daily

Forwarding top(vote > 100) Product Hunt posts to Telegram channel in real time.

## Prerequisites

To deploy the project by yourself, you need to create a Telegram [Channel](https://telegram.org/faq_channels) and [Bot](https://core.telegram.org/bots).

[MemCachier](https://www.memcachier.com/) is using for caching. Other Memcaches are supported also.

All configs and credentials are read from environment variables via dotenv. That is, you need to create a .env file manually and putting all variables inside.

Here is an exmample:

```
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=@your_channel_id
MEMCACHIER_SERVERS=your_memcachier_service
MEMCACHIER_USERNAME=your_memcachier_username
MEMCACHIER_PASSWORD=your_memcachier_password
```

## Install

[virtualenv](https://virtualenv.pypa.io) is recommended for installing:

```
virtualenv -p python3 ENV
source ENV/bin/activate
pip install -r requirements.txt
```

Or you can also use your system Python:

```
pip3 install -r requirements.txt
```

## Run

```
python ph_daily.py
```

For a production environment, [pm2](http://pm2.keymetrics.io/) is recommended:

```
pm2 start ph_daily.py --interpreter ./ENV/bin/python --watch
```

or, with pm2 ecosystem file:

```
pm2 start ecosystem.config.js
```

## Run with Docker

```
docker pull maxhis/ph_daily:1.0.1
docker run --rm --env-file ./.env -t maxhis/ph_daily:1.0.1
```