import pandas as pd
from typing import List, Dict


def load_data(
    sources: List[str],
    storage_options: Dict[str, str]
) -> pd.DataFrame:
    datasets = []
    for source in sources:
        data = pd.read_csv(
            source,
            compression='gzip',
            storage_options=storage_options,
            usecols=['text', 'rating', 'total_votes'],
            nrows=100
        )
        datasets.append(data)
    dataset = pd.concat(datasets, ignore_index=True)
    dataset['positive'] = dataset['rating'] > 5
    dataset = dataset[~dataset['rating'].isna()].drop('rating', axis=1)
    return dataset


def sample_data(
    data: pd.DataFrame,
    frac: float = None,
    n: int = None,
    label: str = 'positive',
    weight: str = 'total_votes'
) -> pd.DataFrame:
    """
    Generate a sample by picking objects with most number of votes from each
    classes. So a review with highest number of votes will be picked first.
    Note: this is not a random sample.     

    Args:
        data (pd.DataFrame): input data
        frac (float, optional): fraction of 
        n (int, optional): _description_. Defaults to None.
        label (str, optional): _description_. Defaults to 'positive'.
        weight (str, optional): _description_. Defaults to 'total_votes'.

    Returns:
        pd.DataFrame: _description_
    """
    data_len = len(data)
    if (not frac and not n) or (frac and n):
        raise ValueError('Either "frac" or "n" must be set.')
    if frac:
        if (frac > 1) or (frac < 0):
            raise ValueError('"frac" must be in range [0, 1]')
        if frac == 1:
            return data
        label_dist = (data[label].value_counts() * frac).astype(int)
        labels_samples = []
        for l, n in label_dist.iteritems():
            sample = data[data[label] == l].nlargest(n, weight)
            labels_samples.append(sample)
        sample_df = pd.concat(labels_samples, ignore_index=True)
    elif n:
        if n < 1:
            raise ValueError('"n" must be in range [1, len(data)]')
        sample_df = (
            data
            .sort_values([label, weight])
            .groupby(label)
            .tail(n)
        )
    return sample_df.sample(frac=1)