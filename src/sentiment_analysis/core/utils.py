import importlib
import pickle
import boto3
import yaml
from typing import Dict, Any
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import accuracy_score


EXCLUDE_STEPS = ['model_meta', 'data']


def create_pipeline(config: Dict[str, Any]) -> Pipeline:
    pipeline = Pipeline([])

    available_steps = [
        s for s in config.keys()
        if s not in EXCLUDE_STEPS
    ]
    for step in available_steps:
        step_config = config[step]
        if step_config['use_flg']:
            step_module = importlib.import_module(step_config['module'])
            step_cls = getattr(step_module, step_config['class'])
            step_hp = step_config['hyperparams']
            if step_hp:
                step_init = step_cls(**step_hp)
            else:
                step_init = step_cls()
            pipeline.steps.append((step, step_init))

    return pipeline


def measure_performance(estimator, X, y, model_nm, train_size=0.8):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size
    )

    print('Performing cross-validation ...')
    cv = cross_validate(
        estimator,
        X_train,
        y_train,
        n_jobs=-1,
        scoring='accuracy',
        return_train_score=True
    )
    val_mean = cv['test_score'].mean()
    print(f'Accuracy of {model_nm} on validation set: {val_mean:.3f}')

    estimator.fit(X_train, y_train)
    test_prediction = estimator.predict(X_test)
    test_score = accuracy_score(y_test, test_prediction)
    print(f'Accuracy of {model_nm} on test set: {test_score:.3f}')


def save_object(object: Any, path: str, credentials: Dict[str, str]):
    """
    Save an object to AWS s3 as pickle file.

    Args:
        object (Any): Any object that could be saved as pickle file
        path (str): Path to save the object. You dont't need to specify
        bucket name here
        credentials (Dict[str, str]): AWS credentials containing the following
        fields under 'aws' section: 'region', 'access_key', 'secret_access_key'
    """
    s3 = boto3.resource(
        's3',
        region_name=credentials['aws']['region'],
        aws_access_key_id=credentials['aws']['access_key'],
        aws_secret_access_key=credentials['aws']['secret_access_key']
    )
    byte_obj = pickle.dumps(object)
    s3.Object(credentials['aws']['bucket'], path).put(Body=byte_obj)


def load_object(path: str, credentials: Dict[str, str]) -> Any:
    """
    Load an object from AWS s3.

    Args:
        path (str): Path to save the object. You dont't need to specify
        bucket name here
        credentials (Dict[str, str]): AWS credentials containing the following
        fields under 'aws' section: 'region', 'access_key', 'secret_access_key'
    """
    s3 = boto3.resource(
        's3',
        region_name=credentials['aws']['region'],
        aws_access_key_id=credentials['aws']['access_key'],
        aws_secret_access_key=credentials['aws']['secret_access_key']
    )
    response = s3.Object(credentials['aws']['bucket'], path).get()
    obj_bytes = response['Body'].read()
    return pickle.loads(obj_bytes)


def load_yaml(path: str, *sections) -> Any:
    with open(path, 'r') as f:
        d = yaml.safe_load(f)
    for s in sections:
        d = d[s]
    return d
