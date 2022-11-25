import os
import sys
import yaml
import pandas as pd
import boto3

sys.path.append(os.path.join('..', 'src'))

from sentiment_analysis.core.utils import create_pipeline, measure_performance
from sentiment_analysis.core.data import load_data, sample_data
from sentiment_analysis.core.utils import save_estimator, load_yaml


CONFIG_PATH = 'config.yaml'
CREDENTIALS_PATH = os.path.join('..', 'credentials.yaml')
MODEL_FOLDER = os.path.join('..', 'data', 'models')
TRAIN_SIZE = 0.8


def train_model():
    config = load_yaml(CONFIG_PATH, 'training')
    credentials = load_yaml(CREDENTIALS_PATH)

    storage_options = {
        'key': credentials['aws']['access_key'],
        'secret': credentials['aws']['secret_access_key']
    }

    model_nm = config['model_meta']['name']
    model_ver = config['model_meta']['version']
    full_model_nm = f'{model_nm}_v{model_ver}'
    save_path = config['model_meta']['path'].format(
        credentials['aws']['bucket']
    )

    data_sources = [
        s.format(credentials['aws']['bucket'])
        for s in config['data']['sources']
    ]
    data = load_data(data_sources, storage_options)
    sample = sample_data(
        data,
        config['data']['frac'],
        config['data']['n']
    )
    X, y = sample['text'], sample['positive']

    pipeline = create_pipeline(config)

    measure_performance(pipeline, X, y, full_model_nm, TRAIN_SIZE)

    pipeline.fit(X, y)
    save_estimator(pipeline, save_path, credentials)
    print(f'Model {full_model_nm} have been saved on S3!')


if __name__ == '__main__':
    train_model()
