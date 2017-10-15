from django.db import models


# Create your models here.


class TwitterEntity(models.Model):
    name = models.CharField(max_length=100, null=True)
    twitter_handle = models.CharField(max_length=100)


class SentimentalAnalysisData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=100, null=True)
    score = models.FloatField()
    magnitude = models.FloatField()
    magnitude_normalized = models.FloatField()
    tweet_count = models.IntegerField()
    twitter_entity = models.ForeignKey(TwitterEntity, on_delete=models.CASCADE)


class User(models.Model):
    device_id = models.CharField(max_length=100)
    fcm_token = models.CharField(max_length=200)


class PendingTweetData(models.Model):
    twitter_entity = models.ForeignKey(TwitterEntity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
