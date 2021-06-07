import logging

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def clean(local_path, enc_features, old_index_col, index_col, store_path, clean_features):
	"""
	clean up raw dataframe and save cleaned data into data folder

	Args:
		local_path (str): file path for raw data
		enc_features (:obj:`list`): list of binary variables that needs to be encodes into 1 or 0
		old_index_col (str): the old index column
		index_col (str): the new index column name
		store_path (str): the path to store cleaned data
		clean_features (:obj:`list`): list of variables in cleaned data

	Returns:
		df (:obj:`DataFrame <pandas.DataFrame>`): the cleaned data
	"""
	try:
		df = pd.read_csv(local_path)
	except FileNotFoundError:
		logger.error("File %s is not found" % local_path)

	df = df.rename(columns={old_index_col: index_col})

	# convert cols to binary
	for var in enc_features:
		df[var] = [np.where("not" in x, 0, 1) for x in df[var]]

	logger.info("Data has %i observations" % df.shape[0])
	logger.info("Data has %i columns" % df.shape[1])

	df = df[clean_features]
	# store cleaned data
	df.to_csv(store_path, index=False)

	return df


def standardization(df, features):
	"""Standardize the cleaned raw dataframe

	Args:
		df (:obj:`DataFrame <pandas.DataFrame>`): the dataframe to be standardized
		features (:obj:`list`): list of features

	Returns:
		df_scale (:obj:`DataFrame <pandas.DataFrame>`): the dataframe after standardized
	"""
	df_scale = df.copy(deep=True)
	feature_df = df_scale[features]
	scaled_features = StandardScaler().fit_transform(feature_df.values)
	df_scale[features] = scaled_features
	return df_scale


def get_standard_scalar(df, features):
	"""get the standard scalar after fitting the given dataframe and features, and the scalar will be used to
	transform user input in modeling phase

	Args:
		df (:obj:`DataFrame <pandas.DataFrame>`): the dataframe for fitting the scalar
		features (:obj:`list`): list of features

	Returns:
		scalar (:obj:'sklearn.preprocessing._data.StandardScaler'): the standard scalar after fitting data
	"""
	df_scale = df.copy(deep=True)
	feature_df = df_scale[features]
	scalar = StandardScaler().fit(feature_df.values)
	return scalar

