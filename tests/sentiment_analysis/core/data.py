import os
import sys
import pytest
import pandas as pd


ROOT_DIR = os.path.join('..', '..', '..', 'src')
sys.path.append(ROOT_DIR)

from sentiment_analysis.core.data import sample_data

@pytest.fixture
def reviews_dataset():
    return pd.DataFrame({
        'text': ['a', 'b', 'c', 'd', 'e', 'ee', 'ff', 'g', 'm', 'mm'],
        'total_votes': [10, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'positive': [True, False, True, False, True,
                    False, True, False, True, False]
    })


def test_sample_data_n(reviews_dataset):
    sample = sample_data(
        reviews_dataset,
        n=2,
        label='positive',
        weight='total_votes'
    )
    assert len(sample) == 4
    assert len(sample[sample['positive'] == True])\
            & len(sample[sample['positive'] == False])

def test_sample_data_frac_part(reviews_dataset):
    sample = sample_data(
        reviews_dataset,
        frac=0.4,
        label='positive',
        weight='total_votes'
    )
    assert len(sample) == 4
    assert (len(sample[sample['positive'] == True]) == 2)\
            & (len(sample[sample['positive'] == False]) == 2)


def test_sample_data_frac_full(reviews_dataset):
    sample = sample_data(
        reviews_dataset,
        frac=1,
        label='positive',
        weight='total_votes'
    )
    assert len(sample) == 10
    assert (len(sample[sample['positive'] == True]) == 5)\
            & (len(sample[sample['positive'] == False]) == 5)
