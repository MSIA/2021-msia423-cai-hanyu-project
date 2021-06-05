import logging

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def clean(local_path, enc_features, old_index_col, index_col, store_path, clean_features):
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
	#store cleaned data
	df.to_csv(store_path,index=False) 

	return df

def standardization(df, features):
	df_scale = df.copy(deep=True)
	feature_df = df_scale[features]
	scaled_features = StandardScaler().fit_transform(feature_df.values)
	df_scale[features] = scaled_features
	return df_scale

def get_standard_scalar(df, features):
	df_scale = df.copy(deep=True)
	feature_df = df_scale[features]
	scalar = StandardScaler().fit(feature_df.values)
	return scalar

