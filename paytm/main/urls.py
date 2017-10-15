from django.conf.urls import url

from paytm.views import SentimentalAnalysisAPIView, TwitterEntitiesAPIView

urlpatterns = [
    url(r'^sentimental_analysis/$', SentimentalAnalysisAPIView.as_view(), name='sentimental_analysis'),
    url(r'^twitter_entities/$', TwitterEntitiesAPIView.as_view(), name='twitter_entities'),
    ]