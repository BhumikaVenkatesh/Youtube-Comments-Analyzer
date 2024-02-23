from googleapiclient.discovery import build
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import re
import streamlit as st
from Comment_analyzer import get_video_id
import warnings
warnings.filterwarnings('ignore')

DEVELOPER_API_KEY='xxxxxxxxxxxxxxxxxxxxx' # Replace with your API key for Youtube Data API
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_API_KEY)


def get_channel_id(video_id):
  video_response = youtube.videos().list(
      part='snippet',
      id=video_id
  ).execute()
  video_snippet = video_response['items'][0]['snippet']
  uploader_channel_id = video_snippet['channelId']
  return uploader_channel_id


def save_comments_to_file(url):
  video_id=get_video_id(url)
  uploader_channel_id=get_channel_id(video_id)
  comments=[]
  nextPageToken=None
  while len(comments)<1000:
    request=youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        pageToken=nextPageToken
    )
    response=request.execute()
    for item in response['items']:
      comment=item['snippet']['topLevelComment']['snippet']
      
  #     eliminating own comments
      if comment['authorChannelId']['value']!=uploader_channel_id:
        comments.append(comment['textDisplay'])
    nextPageToken=response.get('nextPageToken')

    if not nextPageToken:
      break

  hyperlink_pattern=re.compile(
      r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

  threshold_ratio=0.65

  relevant_comments=[]

  for comment_text in comments:
    comment_text=comment_text.lower().strip()
    emojis=emoji.emoji_count(comment_text)
    text_characters=len(re.sub(r'\s','',comment_text))
    if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
      if emojis==0 or (text_characters/(text_characters+emojis))>threshold_ratio:
        relevant_comments.append(comment_text)
    
  filename='ytcomments.txt'
  with open(filename,'w',encoding='utf-8') as f:
    for idx, comment in enumerate(relevant_comments):
      f.write(str(comment)+"\n")  

