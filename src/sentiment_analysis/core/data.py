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
            usecols=['text', 'rating', 'total_votes']
        )
        datasets.append(data)
    return pd.concat(datasets, ignore_index=True)


def sample_data(
    data: pd.DataFrame,
    frac: float = None,
    n: int = None
) -> pd.DataFrame:
    """
    Generate a sample by picking n (or frac * len(data)) objects having most
    votes equally from all classes. So a review with highest number of votes
    will be picked first, etc.
    Note: this is not a random sample. 
    """
    data_len = len(data)
    if not frac and not n:
        raise ValueError('Either "frac" or "n" must be set.')
    if frac:
        if (frac > 1) | (frac < 0):
            raise ValueError('"frac" must be in range [0, 1]')
        n_obj = int(data_len * frac)
    elif n:
        if (n < 1) | (n > data_len):
            raise ValueError('"n" must be in range [1, len(data)]')
        n_obj = n
    sample = (
        data
        .sort_values(['positive', 'total_votes'])
        .groupby('positive')
        .tail(n_obj)
    )
    return sample
