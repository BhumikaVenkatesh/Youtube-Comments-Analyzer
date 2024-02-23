from googleapiclient.discovery import build
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import re
from urllib.parse import urlparse
import streamlit as st

def get_video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]    
    return None



def is_question(text):
  question_pattern = re.compile(r'\?|who|what|when|where|why|how|can|could|may|might|must|should|would')
  match = question_pattern.search(text)
  return match is not None


def sentiment_scores(comment, polarity):
  sentiment_object=SentimentIntensityAnalyzer()
  sentiment_dict=sentiment_object.polarity_scores(comment)
  polarity.append(sentiment_dict['compound'])
  return polarity


def analyze_sentiment():
  polarity=[]
  positive_comments=[]
  negative_comments=[]
  neutral_comments=[]
  questions=[]

  with open("ytcomments.txt",'r',encoding='`utf-8') as f:
    comments=f.readlines()

  for index, items in enumerate(comments):
    polarity=sentiment_scores(items, polarity)
    if is_question(items):
      questions.append(items) 
    if polarity[-1]>0.05:
      positive_comments.append(items)
    elif polarity[-1]<-0.05:
      negative_comments.append(items)
    else:
      neutral_comments.append(items)

  if not positive_comments:
     positive_comments.append("There are no positive comments!")

  if not negative_comments:
     negative_comments.append("There are no negative comments")

  if not neutral_comments:
     neutral_comments.append("There are no neutral comments")

  if not questions:
     questions.append("There are no questions!")           
        
  # avg_polarity=sum(polarity)/len(polarity)
  
  # positive_counts=len(positive_comments)
  # negative_counts=len(negative_comments)
  # neutral_counts=len(neutral_comments)

  return {'positive_comments':positive_comments,'negative_comments':negative_comments,'neutral_comments':neutral_comments,'questions':questions}
