import os
import sys
import yaml
import pickle
import importlib
from sklearn.pipeline import Pipeline

sys.path.append(os.path.join('..', 'src'))


CONFIG_PATH = 'config.yaml'
CREDENTIALS_PATH = os.path.join('..', 'credentials.yaml')
MODEL_FOLDER = os.path.join('..', 'data', 'models')


def train_model():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = yaml.safe_load(f)

    pipeline = Pipeline([])

    available_steps = [s for s in config['training'].keys() if s != 'meta']
    for step in available_steps:
        step_config = config['training'][step]
        if step_config['use_flg']:
            step_module = importlib.import_module(step_config['module'])
            step_cls = getattr(step_module, step_config['class'])
            step_hp = step_config['hyperparams']
            if step_hp:
                step_init = step_cls(**step_hp)
            else:
                step_init = step_cls()
            pipeline.steps.append((step, step_init))
        print(pipeline)

if __name__ == '__main__':
    train_model()
