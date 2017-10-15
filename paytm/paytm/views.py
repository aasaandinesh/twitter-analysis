import ast
import json

import time
from threading import Thread

from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests import Response

from main.models import TwitterEntity, SentimentalAnalysisData, User
from paytm.cities import cities
from google.cloud import language

from paytm.settings import CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

from TwitterSearch import *


class SentimentalAnalysisAPIView(View):
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        se = SentimentalAnalysisData.objects.filter(twitter_entity__twitter_handle=keyword).prefetch_related('twitter_entity')
        data = []
        for s in se:
            d = {'count': s.tweet_count, 'score': s.magnitude * s.score, 'latitude': s.latitude,
                 'longitude': s.longitude, 'city': s.city, 'keyword': s.twitter_entity.twitter_handle}
            data.append(d)
        return HttpResponse(json.dumps(data), content_type="application/json")


class FCMDataAPIView(View):
    def post(self, request, *args, **kwargs):
        device_id = request.data.get('device_id')
        fcm_token = request.data.get('fcm_token')
        user_list = User.objects.filter(device_id=device_id)
        if user_list.count() == 0:
            user = User()
            user.device_id = device_id
            user.fcm_token = fcm_token
            user.save()
            return HttpResponse(json.dumps(user), content_type="application/json")
        else:
            user = user_list.first()
            user.fcm_token = fcm_token
            user.save()
            return HttpResponse(json.dumps(user), content_type="application/json")


def get_twitter_object(t):
    return {'keyword': t.twitter_handle}


def get_twitter_list(twitter_list):
    data = []
    for t in twitter_list:
        data.append(get_twitter_object(t))
    return data



class TwitterEntitiesAPIView(View):
    def get(self, request, *args, **kwargs):
        print("Check if this is getting printed")
        return HttpResponse(json.dumps(get_twitter_list(TwitterEntity.objects.all())),
                            content_type="application/json")

    def post(self, request, *args, **kwargs):
        keyword = json.loads(request.body.decode('utf-8')).get('keyword')
        t = None
        if not TwitterEntity.objects.filter(twitter_handle=keyword).exists():
            t = TwitterEntity()
            t.twitter_handle = keyword
            t.name = keyword
            t.save()
        else:
            t = TwitterEntity.objects.filter(twitter_handle=keyword).first()
        thread = Thread(target=run_sentimental_analysis, args=(t,))
        thread.start()
        print("Thread should have started by now..")
        return HttpResponse(json.dumps(get_twitter_object(t)), content_type="application/json")


def callback_closure(current_ts_instance):  # accepts ONE argument: an instance of TwitterSearch
    queries, tweets_seen = current_ts_instance.get_statistics()
    if queries > 0 and (queries % 5) == 0:  # trigger delay every 5th query
        print('Going off to sleep for 60 seconds')
        time.sleep(60)  # sleep for 60 seconds


def run_sentimental_analysis(twitter_obj):
    print("Starting the analysis part")
    print("This might take about half an hour")
    for city in cities:
        print('Starting things for city: ' + city['name'])
        tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
        tso.set_keywords([twitter_obj.twitter_handle])  # let's define all words we would like to have a look for
        city['lat'] = float(city['lat'])
        city['lon'] = float(city['lon'])
        tso.set_geocode(city['lat'], city['lon'], 200)
        tso.set_language('en')

        print('doing stuffs for city ' + city['name'])

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        print('Prepared for sending Tweet request.....')
        full_text = ''
        count = 0
        for tweet_object in ts.search_tweets_iterable(tso, callback=callback_closure):
            print('Done for tweet #' + str(count))
            full_text += tweet_object['text'] + '.'
            count += 1
            if count >= 999:
                break

        print('Single Text converted.')
        print('Now starting the NLP part...')
        print('This might take some time.......')
        client = language.LanguageServiceClient()

        document = language.types.Document(content=full_text, type='PLAIN_TEXT')
        response = client.analyze_sentiment(document=document, encoding_type='UTF32')
        sentiment = response.document_sentiment
        print('Got response from NLP part')
        print('Now saving the result in the DB...')
        sentiment_object = SentimentalAnalysisData()
        sentiment_object.latitude = city['lat']
        sentiment_object.longitude = city['lon']
        sentiment_object.city = city['name']
        sentiment_object.score = sentiment.score
        sentiment_object.magnitude = sentiment.magnitude
        sentiment_object.twitter_entity = twitter_obj
        sentiment_object.tweet_count = count
        if count > 0:
            sentiment_object.magnitude_normalized = sentiment.magnitude / count
        else:
            sentiment_object.magnitude_normalized = 0
        sentiment_object.save()
        print('Voila! Done for City ' + city['name'])
    print('Phew..! Finally completed!')


def handle_request(twitter_handle, name=None):
    twitter_entities_list = TwitterEntity.objects.filter(twitter_handle=twitter_handle).all()
    if len(twitter_entities_list) == 0:
        twitter_entity = TwitterEntity()
        twitter_entity.name = name
        twitter_entity.twitter_handle = twitter_handle
        twitter_entity.save()
        twitter_obj = twitter_entity
    else:
        twitter_obj = twitter_entities_list.first()
    run_sentimental_analysis(twitter_obj)
