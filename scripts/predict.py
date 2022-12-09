print('Hello, World!')
import os
print(os.getenv('AWS_BUCKET'))
# import os
# import sys
# import argparse

# sys.path.append(os.path.join('..', 'src'))

# import pandas as pd
# from sentiment_analysis.core.utils import load_object, load_yaml


# CONFIG_PATH = 'config.yaml'
# CREDENTIALS_PATH = os.path.join('..', 'credentials.yaml')
# MODEL_FOLDER = os.path.join('..', 'data', 'models')


# if __name__ == '__main__':
#     config = load_yaml(CONFIG_PATH, 'training')
#     credentials = load_yaml(CREDENTIALS_PATH)

#     storage_options = {
#         'key': credentials['aws']['access_key'],
#         'secret': credentials['aws']['secret_access_key']
#     }

#     model_nm = config['model_meta']['name']
#     model_ver = config['model_meta']['version']
#     full_model_nm = f'{model_nm}_v{model_ver}'
#     save_path = config['model_meta']['path'].format(full_model_nm)

#     pipeline = load_object(save_path, credentials)

#     reviews = [
#         'Very good review! Awesome! The movie is so good I recommend it to all my friends',
#         'No, I do not want to continue watching this movie. It is terrible'
#     ]
#     pred_label = pipeline.predict(reviews)
#     pred_prob = pipeline.predict_proba(reviews)
#     pred = [
#         {'label': l, 'probability': p.max()}
#         for l, p in zip(pred_label, pred_prob)
#     ]
#     print(pred)
