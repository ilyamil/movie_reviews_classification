import tweepy

credentials_file = os.path.abspath(os.path.join('..', 'credentials.yaml'))
with open(credentials_file, 'r') as f:
    credentials = yaml.safe_load(f)

storage_options = {
    'key': credentials['aws']['access_key'],
    'secret': credentials['aws']['secret_access_key']
}

tweepy_client = tweepy.Client(credentials['twitter']['bearer_token'])
tw = tweepy_client.get_tweet(1591500826312318977)
tw.data