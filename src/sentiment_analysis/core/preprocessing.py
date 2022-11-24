import re
import nltk
import pandas as pd
from typing import List, Tuple
from sklearn.base import BaseEstimator, TransformerMixin


nltk.download([
    'stopwords',
    'punkt',
    'wordnet',
    'omw-1.4',
    'averaged_perceptron_tagger'],
    quiet=True
)

TAGS = {
    "J": nltk.corpus.wordnet.ADJ,
    "N": nltk.corpus.wordnet.NOUN,
    "V": nltk.corpus.wordnet.VERB,
    "R": nltk.corpus.wordnet.ADV
}
STOPWORDS = set(nltk.corpus.stopwords.words("english"))


def preprocess_data(data: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Removes objects without rating and creates target variable column.
    """
    data_ = data.copy()
    data_['positive'] = data_['rating'] > 5
    data_ = data_[~data_['rating'].isna()].drop('rating', axis=1)
    return data_['text'], data_['positive']


class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        use_lemmatizer: bool = True,
        use_lowercase: bool = True,
        remove_stopwords: bool = True
    ):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.tokenizer = re.compile(r'\w+')
        self.use_lemmatizer = use_lemmatizer
        self.use_lowercase = use_lowercase
        self.remove_stopwords = remove_stopwords

    def _tokenize(self, doc: str) -> List[str]:
        return self.tokenizer.findall(doc)

    def _get_lemma(self, word: str, tag: str) -> str:
        if tag[0] not in TAGS.keys():
            return self.lemmatizer.lemmatize(word)
        return self.lemmatizer.lemmatize(word, TAGS[tag[0]])

    def _transform(self, doc: str) -> List[str]:
        tokens = self._tokenize(doc)
        
        if self.use_lowercase:
            tokens = [t.lower() for t in tokens]
        
        if self.use_lemmatizer:
            tags = nltk.pos_tag(tokens)
            tokens = [self._get_lemma(token, tag) for token, tag in tags]

        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in STOPWORDS]

        return ' '.join(tokens)

    def fit(self, X=None, y=None):
        return self

    def transform(self, X: pd.Series) -> pd.Series:
        return X.apply(self._transform)
