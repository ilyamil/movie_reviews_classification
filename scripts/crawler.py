import os
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from sentiment_analysis.core.utils import load_yaml
from sentiment_analysis.crawler.tweets import load_tweets


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


def run():
    config = load_yaml(CONFIG_FILE, 'crawler')
    sources = load_yaml(SOURCES_FILE, 'sources')
    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - relativedelta(minutes=config['frequency'])
    tweets = load_tweets(
        token=os.getenv('TWITTER_BEARER_TOKEN'),
        user_id=[v['twitter_id'] for v in sources.values()],
        max_results=5,
        start_dt=start_dt,
        end_dt=end_dt
    )
    print(len(tweets), tweets['user_id'].nunique())


if __name__ == '__main__':
    run()
