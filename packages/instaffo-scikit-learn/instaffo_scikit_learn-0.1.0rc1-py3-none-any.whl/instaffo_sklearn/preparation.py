"""
This module contains classes involved in the preparation process in
machine learning pipelines. This involves for examples aggregating values
and pivotizing tables.
"""
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from pandas.api.types import CategoricalDtype
import numpy as np


class Aggregator(BaseEstimator, TransformerMixin):
    """
    This class aggregates the values of a long data frame,
    provided a column name to group by, a column name with values to aggregate
    and a method to aggregate with.

    Args:
        col (str, optional): the name of the column to group by.
        val (str, optional): the name of the col that contains the val.
        aggfunc (callable, optional): the method to be applied to the grouped val.

    Attributes:
        col (str): the name of the col to group by.
        val (str): the name of the col that contains the val.
        aggfunc (callable): the method to be applied to the grouped val.
    """

    def __init__(self, col="col", val="val", aggfunc=np.sum):
        self.col = col
        self.val = val
        self.aggfunc = aggfunc

    def fit(self, X=None, y=None):
        """
        Fits the transformer to the data.

        Args:
            X (None): should be None to be compliant with sklearn API.
            y (None): should be None to be compliant with sklearn API.

        Returns:
            Aggregator: an Aggregator object.
        """
        return self

    def transform(self, X, y=None):
        """
        Aggregates the data frame.

        Args:
            X (pandas.DataFrame): a data frame that should be aggregated.
            y (None): should be None to be compliant with sklearn API.

        Returns:
            pandas.DataFrame: the aggregated data frame.
        """
        X_transformed = X.copy()
        X_transformed = (
            X_transformed.groupby(self.col)[self.val].agg(self.aggfunc).reset_index()
        )
        return X_transformed


class Pivotizer(BaseEstimator, TransformerMixin):
    """
    This class converts a dataframe from long to wide format.
    It is similar to pandas.DataFrame.pivot but can work with sparse data.
    Part of the source code for this class was taken from:
    https://stackoverflow.com/a/31679396.

    Args:
        row (str): the name of the col that should be put on the rows.
        col (str): the name of the col that should be put as cols.
        val (str): the name of the col that should be put inside the cells.

    Attributes:
        row (str): the name of the col that should be put on the rows.
        col (str): the name of the col that should be put as cols.
        val (str): the name of the col that should be put inside the cells.
        row_cat (pandas.api.types.CategoricalDtype): the rows of the pivoted table.
        col_cat (pandas.api.types.CategoricalDtype): the cols of the pivoted table.
    """

    def __init__(self, row="row", col="col", val="val"):
        self.row = row
        self.col = col
        self.val = val
        self.row_cat = None
        self.col_cat = None

    def fit(self, X, y=None):
        """
        Fits the transformer.

        Args:
            X (pandas.DataFrame): a data frame.
            y (None, optional): should be None to be compliant with sklearn API.

        Returns:
            PivotSparse: returns itself to conform with sklearn api.
        """
        self.col_cat = CategoricalDtype(sorted(X[self.col].unique()), ordered=True)
        return self

    def transform(self, X, y=None):
        """
        Pivotizes a provided data frame.

        Args:
            X (pandas.DataFrame): a data frame.
            y (None, optional): should be None to be compliant with sklearn API.

        Returns:
            scipy.sparse.csr_matrix: a pivoted matrix.
        """

        X_transformed = X[X[self.col].isin(self.col_cat.categories)]

        self.row_cat = CategoricalDtype(
            sorted(X_transformed[self.row].unique()), ordered=True
        )

        row = X_transformed[self.row].astype(self.row_cat).cat.codes
        col = X_transformed[self.col].astype(self.col_cat).cat.codes

        X_transformed = csr_matrix(
            (X_transformed[self.val], (row, col)),
            shape=(self.row_cat.categories.size, self.col_cat.categories.size),
        )

        return X_transformed
