import json
from threading import Thread

from flask import current_app, render_template, copy_current_request_context
from flask_socketio import emit
from shapely.geometry import mapping, shape
import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

from app import socketio
from app.main import bp





def get_centroid(polygon):
    """
    params polygon: GeoJson polygon
    return: GeoJson Point
    """
    polygon = shape(polygon)
    point = polygon.centroid
    return mapping(point)

def parser(tweet):
    """
    params tweet: dict
    return: GeoJson dict
    """
    geoJson = {
        "type": "Feature",
        "properties": {
            "text": tweet['text'],
            "created_at": tweet['created_at'].split('+')[0],
            "user": "@" + tweet['user']['screen_name']
        },
        "geometry": get_centroid(tweet['place']['bounding_box'])
    }

    return geoJson


class MyListener(StreamListener):
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        try:
            if 'place' in data and data['place']:  # Only tweets with location info
                feature = parser(data)
                socketio.emit('addMarker', feature, json=True)  # Send the tweet to all connected clients
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

@bp.before_app_first_request
def start_filter_threadpool():
    @copy_current_request_context
    def start_filter_thread():
        auth = OAuthHandler(current_app.config.get("CONSUMER_KEY"), current_app.config.get("CONSUMER_SECRET"))
        auth.set_access_token(current_app.config.get("ACCESS_TOKEN"), current_app.config.get("ACCESS_SECRET"))
        api = tweepy.API(auth)
        tags = current_app.config.get('TAGS') or ['#coronavirus']
        twitter_stream = Stream(auth, MyListener())  # Create object for Twitter Streaming API
        twitter_stream.filter(track=tags) # Start getting all the tweets with the given tags
    thread = Thread(target=start_filter_thread)
    thread.daemon = True
    thread.start()

@bp.route('/')
def index():
    return render_template('index.html')
