import os
import sys
import yaml
import pandas as pd

sys.path.append(os.path.join('..', 'src'))

from sentiment_analysis.core.utils import create_pipeline, measure_performance
from sentiment_analysis.core.data import load_data, sample_data
from sentiment_analysis.core.preprocessing import preprocess_data


CONFIG_PATH = 'config.yaml'
CREDENTIALS_PATH = os.path.join('..', 'credentials.yaml')
MODEL_FOLDER = os.path.join('..', 'data', 'models')
TRAIN_SIZE = 0.8


def train_model():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = yaml.safe_load(f)

    storage_options = {
        'key': credentials['aws']['access_key'],
        'secret': credentials['aws']['secret_access_key']
    }

    full_model_nm = (
        config['training']['model_meta']['name']
        + '_'
        + str(config['training']['model_meta']['version'])
    )

    # data_sources = [
    #     s.format(credentials['aws']['bucket'])
    #     for s in config['training']['data']['sources']
    # ]
    # data = load_data(data_sources, storage_options)
    # sample = sample_data(
    #     data,
    #     config['training']['data']['frac'],
    #     config['training']['data']['n']
    # )
    # X, y = preprocess_data(sample)

    pipeline = create_pipeline(config)
    print(full_model_nm, pipeline)

    measure_performance(pipeline, X, y, TRAIN_SIZE)

    # # pipeline.fit(X, y)

    # print(f'Model {full_model_nm} have been saved on S3!')

if __name__ == '__main__':
    train_model()
