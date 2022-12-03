import os
import argparse
from sentiment_analysis.core.utils import (
    create_pipeline,
    measure_performance,
    save_object,
    load_yaml
)
from sentiment_analysis.core.data import load_data, sample_data


CONFIG_PATH = 'config.yaml'
CREDENTIALS_PATH = os.path.join('..', 'credentials.yaml')
MODEL_FOLDER = os.path.join('..', 'data', 'models')
TRAIN_SIZE = 0.8


def parse_train_cli_arguments():
    parser = argparse.ArgumentParser(
        'Model Trainer',
        description=(
            'Train machine learning model to perform sentiment analysis'
        )
    )
    parser.add_argument(
        '-m',
        type=bool,
        default=True,
        help=(
            'Boolean flag to indicate whethere the program needs to do '
            'cross-validation. If set to True, it takes 2-3 times more '
            'time to finish the script.'
        )
    )
    return parser.parse_args()


def train_model(measure_performance_flg: bool = True):
    config = load_yaml(CONFIG_PATH, 'training')
    credentials = load_yaml(CREDENTIALS_PATH)

    storage_options = {
        'key': credentials['aws']['access_key'],
        'secret': credentials['aws']['secret_access_key']
    }

    model_nm = config['model_meta']['name']
    model_ver = config['model_meta']['version']
    full_model_nm = f'{model_nm}_v{model_ver}'
    save_path = config['model_meta']['path'].format(full_model_nm)

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

    if measure_performance_flg:
        measure_performance(pipeline, X, y, full_model_nm, TRAIN_SIZE)

    pipeline.fit(X, y)
    save_object(pipeline, save_path, credentials)
    print(f'Model {full_model_nm} is saved on S3!')


if __name__ == '__main__':
    arguments = parse_train_cli_arguments()
    train_model(arguments.m)
