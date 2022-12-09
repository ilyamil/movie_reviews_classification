import os
import yaml


with open('credentials.yaml', 'r') as f:
    creds = yaml.safe_load(f)
command = 'conda env config vars set'
os.system(f"{command} AWS_ACCESS_KEY={creds['aws']['access_key']}")
os.system(f"{command} AWS_SECRET_ACCESS_KEY={creds['aws']['secret_access_key']}") # noqa
os.system(f"{command} AWS_BUCKET={creds['aws']['bucket']}")
os.system(f"{command} AWS_REGION={creds['aws']['region']}")
os.system(f"{command} TWITTER_API_KEY={creds['twitter']['api_key']}")
os.system(f"{command} TWITTER_API_SECRET_KEY={creds['twitter']['api_secret_key']}") # noqa
os.system(f"{command} TWITTER_BEARER_TOKEN={creds['twitter']['bearer_token']}")
