# Tweet Locator

## Remark
This work is heavily clone from [Tweet-Locator](https://github.com/JuanBenitez97/Tweet-Locator)
By Juan Benitez from this post on [DEV.TO](https://dev.to/juanbenitez97/simple-tweet-locator-using-python-flask-socketio-and-tweepy-49p5)

## Installation
```
git clone https://github.com/phondanai/tweet-locator
cd tweet-locator
pip install -r requirements.txt
```

After this proccess is done you need to create a .env file to store all your secret tokens and being able to use the Twitter APIs, this file should be in the root folder.
```
# file: .env
CONSUMER_KEY = 'Your API KEY'
CONSUMER_SECRET = 'Your API SECRET KEY'
ACCESS_TOKEN = 'Your Access Token'
ACCESS_SECRET = 'Your Access Secret Token'

# You can add more tags to follow in config.py
# file: config.py
TAGS = ["#yourtag", "#youwant" ,"#totrack"]
```

## Run
At the time I post eventlet have some problem with Python 3.7 and 3.8.
Assume you have run with Python 3.6 (not testing with 3.5 yet)
```
gunicorn --worker-class eventlet -w 1 application:app
# or
docker built -t tweet-locator .
docker run -p 8000:8000 tweet-locator
```
