import os
import sys
import tweepy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3].as_posix()
SRC = os.path.join(ROOT, 'src')
os.chdir(ROOT)
sys.path.append(SRC)

from sentiment_analysis.core.utils import load_yaml


CREDENTIALS = 'credentials.yaml'

credentials = load_yaml(CREDENTIALS)
storage_options = {
    'key': credentials['aws']['access_key'],
    'secret': credentials['aws']['secret_access_key']
}

tweepy_client = tweepy.Client(credentials['twitter']['bearer_token'])
tw = tweepy_client.get_users_tweets('WSJ', max_results=10)
print(tw)