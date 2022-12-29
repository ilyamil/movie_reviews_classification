from codecs import ignore_errors
import os
import warnings
import boto3
from argparse import ArgumentParser
from dotenv import load_dotenv
from sentiment_analysis.core.data import load_reviews, sample_data
from sentiment_analysis.core.utils import write_data_to_s3
from sentiment_analysis.core.preprocessing import TextPreprocessor

warnings.filterwarnings('ignore')
load_dotenv()

BUCKET = os.getenv('AWS_BUCKET')
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

DATASET_PARTITIONS = [
    'reviews/reviews_partition_1.csv',
    # 'reviews/reviews_partition_2.csv',
    # 'reviews/reviews_partition_3.csv',
]


argparser = ArgumentParser(
    description="""
    Creates preprocessed dataset with movie reviews.
    Note: raw movie reviews are stored in AWS s3 bucket.

    The final dataset contains two columns:
        1. text: str - preprocessed reviews.
        2. positivity: bool - whether an object represents a positive review
           (labeled as 1) or negative (labeled as 0)

    Preprocessing steps:
        1. Removing URLs
        2. Converting to lowercase
        3. Lemmatizing
        4. Removing stopwords
    """
)
argparser.add_argument(
    '-s', '--sample_size',
    type=int, help='Number of objects in each class'
)
argparser.add_argument(
    '-m', '--mode', choices=['local', 's3'],
    type=str, help='Where to save dataset'
)


def main():
    args = argparser.parse_args()

    reviews = load_reviews(DATASET_PARTITIONS, S3_CLIENT, BUCKET)
    print('Total number of polar reviews:', len(reviews))

    sample = sample_data(reviews, n=args.sample_size)
    print('Number of sampled reviews (in all classes):', len(sample))

    print('Preprocessing reviews...')
    sample['text'] = TextPreprocessor().transform(sample['text'])
    print('Preprocessing completed')

    key = f'movie_reviews_wn_{len(sample)}.csv'
    if args.mode == 'local':
        path = os.path.join('data', 'preprocessed', key)
        sample.to_csv(path, compression='gzip', index=False)
    elif args.mode == 's3':
        path = os.path.join('datasets', key)
        write_data_to_s3(
            s3_client=S3_CLIENT,
            data=sample,
            bucket=AWS_BUCKET,
            key=path,
            format='csv',
            compression='gzip'
        )
    print(f'Reviews dataset is saved in {args.mode} mode with name: {path}')


if __name__ == '__main__':
    main()
