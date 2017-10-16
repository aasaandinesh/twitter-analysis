# Twitter Analysis

**Aim**
Aim is to find out the distribution of emotions over a particular topic across various parts of the country. For example, we need to find out reaction of people on **GST** across country. We can simply analyse what sort of Tweets people are making from different parts of the country. This would give us some understanding of the acceptance level of GST.

You can use this app to get info about anything, be it a Movie review, 

**Process**
* I have used Twitter API to go through thousands of tweets made recently about a particular topic. 
* Analyse those tweets using Machine Learning to assign them a score of Positivity, Negativity,  Neutral or Mixed
* Draw simple Colored Circles to specify the mood of people while making Tweets

**Main Technologies used**

* [Google NLP API](https://cloud.google.com/natural-language/)
* [Twitter Search API](https://developer.twitter.com/en/docs/tweets/search/overview/basic-search) 
* [Django](https://www.djangoproject.com/) For developing the entire Backend


To run the project you would need secrets.json file in this format and keep it in the paytm app
```
{
  "CONSUMER_KEY" : <Twitter Consumer Key>,
  "CONSUMER_SECRET" : <Twitter Consumer Seret Key>,,
  "ACCESS_TOKEN" : <Twitter Access Token>,,
  "ACCESS_TOKEN_SECRET" : <Twitter Access Token Secret>,,
  "DB_USER": <Postgres User>,
  "DB_PASSWORD": <Postgres password>
}
```
