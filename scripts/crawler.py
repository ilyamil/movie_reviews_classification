import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from sentiment_analysis.core.utils import (
    load_yaml,
    write_data_to_s3,
    read_data_from_s3,
    check_file
)
from sentiment_analysis.crawler.tweets import load_tweets


load_dotenv()


CONFIG_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    'scripts',
    'config.yaml'
)
SOURCES_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    'data',
    'sources.yaml'
)
TWITTER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
AWS_BUCKET = os.getenv('AWS_BUCKET')
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY = os.getenv('AWS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    config=boto3.session.Config(signature_version='s3v4')
)


def run(*args):
    # loading config files
    config = load_yaml(CONFIG_FILE, 'crawler')
    sources = load_yaml(SOURCES_FILE, 'sources')

    # data collection
    freq = config['frequency']
    end_dt = pd.Timestamp.now('utc').floor(f'{freq}min')
    start_dt = end_dt - pd.offsets.Minute(freq)
    user_id = [s['twitter_id'] for s in sources.values()]
    tweets = load_tweets(
        token=TWITTER_TOKEN,
        user_id=user_id,
        max_results=config['max_tweets_per_user'],
        start_dt=start_dt.to_pydatetime(),
        end_dt=end_dt.to_pydatetime()
    )

    # data store
    data_key = config['path_template'].format(end_dt.strftime('%Y%m%d%H%M%S'))
    write_data_to_s3(S3_CLIENT, tweets, AWS_BUCKET, data_key, format='csv')

    # log store
    log_key = config['updates_path']
    updates_file_exist = check_file(
        S3_CLIENT,
        AWS_BUCKET,
        log_key
    )
    dtype = {
        'start_dt': 'datetime64[ns, UTC]',
        'end_dt': 'datetime64[ns, UTC]',
        'update_dt': 'datetime64[ns, UTC]',
        'num_records': 'int',
        'file_path': 'str'
    }
    if updates_file_exist:
        records = read_data_from_s3(
            S3_CLIENT,
            AWS_BUCKET,
            log_key,
            format='csv'
        ).astype(dtype)
    else:
        records = pd.DataFrame(columns=dtype.keys()).astype(dtype)

    new_record = pd.DataFrame({
        'start_dt': [start_dt],
        'end_dt': [end_dt],
        'update_dt': [pd.Timestamp.now('utc')],
        'num_records': [len(tweets)],
        'file_path': [data_key]
    }).astype(dtype)

    updates = pd.concat([records, new_record], ignore_index=True)
    write_data_to_s3(S3_CLIENT, updates, AWS_BUCKET, log_key, format='csv')


if __name__ == '__main__':
    run()
