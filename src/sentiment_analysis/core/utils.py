import importlib
import pickle
from typing import Dict, Any
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import accuracy_score


EXCLUDE_STEPS = ['model_meta', 'data']


def create_pipeline(config: Dict[str, Any]) -> Pipeline:
    pipeline = Pipeline([])

    available_steps = [
        s for s in config['training'].keys()
        if s not in EXCLUDE_STEPS
    ]
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

    return pipeline


def measure_performance(estimator, X, y, model_nm, train_size=0.8):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size
    )

    cv = cross_validate(
        estimator,
        X_train,
        y_train,
        n_jobs=-1,
        scoring='accuracy',
        return_train_score=True
    )
    val_mean = cv['test_score'].mean()
    val_std = cv['test_score'].std()
    print(
        f'Accuracy of {model_nm} on validation set:',
        f'{val_mean:.3f} +/- {val_std:.3f}',
        sep='\n'
    )

    estimator.fit(X_train, y_train)
    test_prediction = estimator.predict(X_test)
    test_score = accuracy_score(y_test, test_prediction)
    print(f'Accuracy of {model_nm} on test set: {test_score:.3f}')


def save_estimator(estimator, path):
    pass