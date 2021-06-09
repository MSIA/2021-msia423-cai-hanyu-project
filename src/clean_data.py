import logging

import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def read_data(local_path, index_col_num):
    """Read in data and return the dataframe"""
    try:
        data = pd.read_csv(local_path, index_col=[index_col_num])
    except FileNotFoundError:
        logger.error("File %s is not found", local_path)

    return data


def clean(data, enc_features, store_path, clean_features, binary_word):
    """
    clean up raw dataframe and save cleaned data into data folder

    Args:
        data (:obj:`DataFrame <pandas.DataFrame>`): the raw data
        enc_features (:obj:`list`): list of binary variables that needs to be encodes into 1 or 0
        store_path (str): the path to store cleaned data
        clean_features (:obj:`list`): list of variables in cleaned data
        binary_word (str): the word for binary conversion

    Returns:
        data (:obj:`DataFrame <pandas.DataFrame>`): the cleaned data
    """

    # convert binary cols to 1 or 0
    for var in enc_features:
        data[var] = data[var].apply(lambda x: 0 if binary_word in x else 1)

    logger.info("Data has %i observations", data.shape[0])
    logger.info("Data has %i columns", data.shape[1])

    # only store columns that will be used in following stages
    data = data[clean_features]

    # store cleaned data
    data.to_csv(store_path, index=False)
    logger.info('Data is saved to path %s', store_path)

    return data


def standardization(data, features):
    """Standardize the cleaned raw dataframe

    Args:
        data (:obj:`DataFrame <pandas.DataFrame>`): the dataframe to be standardized
        features (:obj:`list`): list of features

    Returns:
        df_scale (:obj:`DataFrame <pandas.DataFrame>`): the dataframe after standardized
    """
    df_scale = data.copy(deep=True)
    feature_df = df_scale[features]
    scaled_features = StandardScaler().fit_transform(feature_df.values)
    df_scale[features] = scaled_features
    return df_scale


def get_standard_scalar(data, features):
    """get the standard scalar after fitting the given dataframe and features, and the scalar will
    be used to transform user input in modeling phase

    Args:
        data (:obj:`DataFrame <pandas.DataFrame>`): the dataframe for fitting the scalar
        features (:obj:`list`): list of features

    Returns:
        scalar (:obj:'sklearn.preprocessing._data.StandardScaler'): the standard scalar after
        fitting data
    """
    df_scale = data.copy(deep=True)
    feature_df = df_scale[features]
    scalar = StandardScaler().fit(feature_df.values)
    return scalar

