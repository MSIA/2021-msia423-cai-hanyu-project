import logging

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, pairwise_distances

from src.clean_data import standardization,get_standard_scalar

from joblib import dump, load


logger = logging.getLogger(__name__)


def generate_kmeans(df, features, n_cluster, seed, model_save_path):
	"""Initialize the k-means clustering model

	Args:
		df (:obj:`DataFrame <pandas.DataFrame>`): the data used for generate k means clustering
		features (:obj:`list`): list of features
		n_cluster (int): number of clusters
		seed (int): the random state
		model_save_path (str): the path to save k means model

	Returns:
		model (:obj:`joblib`): the k means clustering model
	"""
	scale_df = standardization(df, features)
	model = KMeans(n_clusters=n_cluster, random_state=seed).fit(scale_df[features])

	# model evaluation
	si = silhouette_score(scale_df[features], model.labels_)
	if si >= 0.4:
		logger.info('The model has silhouette score %f' % si)
	else:
		logger.warning('The model has silhouette score %f , and the model may not distinguish different products well' % si)

	# save model to joblib
	dump(model, model_save_path) 

	return model
	
	
def predict_user_input(data, user_input, model_save_path, store_path, features, top, clean_vars, web_display_vars,
					   	cluster_labels='cluster_label', bar_index='index', preset_index='999999'):
	"""Cluster the user input product information and format the prediction result

	Args:
		data (:obj:`DataFrame <pandas.DataFrame>`): the records of chocolate bars
		user_input (:obj:`DataFrame <pandas.DataFrame>`): one row dataframe that contains user input
		model_save_path (str): path for the model joblib file
		store_path (str): the path to store the recommendation table
		features (:obj:`list`): the list of features for recommendation generation
		top (int) : choose the top n products for recommendation
		clean_vars (:obj:`list`): the list of features stored in cleaned data
		web_display_vars (:obj:`list`): the list of features used for display on webpage
		cluster_labels (str): the column name for storing cluster label
		bar_index (str): the column name for chocolate bar index
		preset_index (str): the preset index for user input chocolate bar information

	Returns:
		result (:obj:`DataFrame <pandas.DataFrame>`): the recommendation table
	"""
	df = data[clean_vars]
	df_web_display = data[web_display_vars]
	scale_df = standardization(df, features)
	model = load(model_save_path)

	# scale and concat user input data
	scale_user_array = get_standard_scalar(df, features).transform(user_input[features])
	scale_user= user_input.copy(deep=True)
	scale_user[features] = scale_user_array

	# concat data with new user input
	df = pd.concat([df, user_input])
	scale_df = pd.concat([scale_user, scale_df])

	# prediction
	df[cluster_labels] = model.predict(scale_df[features])
	
	logger.info('The user input is classified as %i' % int(df[df[bar_index] == preset_index][cluster_labels]))
	result = formatting_preds(df, df_web_display, features, top, store_path)

	return result


def get_userinput(cocoa, rating, beans, cocoa_butter, vanilla, lecithin, salt, sugar, sweetener_without_sugar,
				  input_cols, preset_index, replace_dict):
	"""Formatting user input data from flask app

	Args:
		cocoa (float): the percentage of cocoa for chocolate bar
		rating (float): the rating given by the user
		beans (str): whether the chocolate bar contains beans
		cocoa_butter (str): whether the chocolate bar contains cocoa butter
		vanilla (str): whether the chocolate bar contains vanilla
		lecithin (str): whether the chocolate bar contains lecithin
		salt (str): whether the chocolate bar contains salt
		sugar (str): whether the chocolate bar contains sugar
		sweetener_without_sugar (str): sweetener_without_sugar
		input_cols (:obj:`list`): the list of features in user input
		preset_index (str): the preset index for user input product
		replace_dict (:obj:`dictionary`): the dictionary that map 'yes' and 'no' into 1 and 0

	Returns:
		input_value (:obj:`DataFrame <pandas.DataFrame>`): the well-formatted dataframe that contains user input
	"""
	input_value = pd.DataFrame([[preset_index, cocoa, rating, beans, cocoa_butter, vanilla, lecithin, salt, sugar,
								 sweetener_without_sugar]], columns=input_cols)
	input_value = input_value.replace(replace_dict)

	return input_value


def formatting_preds(preds, raw_df, features, top, store_path, choco_index='index', user_input_index='999999',
						cluster_labels='cluster_label', rec_product_name='chocolate_bar', rank_name='rank',
						join_method='inner', drop_idx1='index_x', drop_idx2='index_y'):
	"""Formatting prediction dataframe, calculate the relative distance matrix, and generate a
	recommendation table with top 10 recommended products

	Args:
		preds (:obj:`DataFrame <pandas.DataFrame>`): the dataframe that contain cluster label
		raw_df (:obj:`DataFrame <pandas.DataFrame>`): the raw dataframe that contain raw features
		features (:obj:`list`): the list of features in preds dataframe
		top (int): the top n products to be recommended
		store_path (str): the path that store recommendation table
		choco_index (str): the index column name
		user_input_index (str): the value for user input in the index column
		cluster_labels (str): the column name for cluster label
		rec_product_name (str): the name of product to be recommended
		rank_name (str): the rank of products to be recommended
		join_method (str): the join method for merging prediction dataframe with raw dataframe
		drop_idx1 (str): the 1st index column to be dropped after merging
		drop_idx2 (str): the 2nd index column to be dropped after merging

	Returns:
		rec_result (:obj:`DataFrame <pandas.DataFrame>`): the recommendation table
	"""
	# get distance matrix
	input_cluster = int(preds[preds[choco_index] == user_input_index][cluster_labels])
	clusters = preds[preds[cluster_labels] == input_cluster].reset_index(drop=True)
	dist_matrix = pairwise_distances(clusters[features])

	# get top n chocolate bars for user input
	top_recs = np.argsort(dist_matrix)[:, :(top + 1)]
	ref_dicts = preds[choco_index].to_dict()
	vectorization = np.vectorize(ref_dicts.get)(top_recs)
	df_recs = pd.DataFrame(vectorization, columns=[choco_index] + [f'chocolate{i}' for i in range(1, 11)])
	df_recs = df_recs[df_recs[choco_index] == user_input_index]

	# melt and map result dataframe
	melts = melting_dataset(df_recs, choco_index, rank_name, rec_product_name)
	rec_result = mapping(melts, rec_product_name, raw_df, choco_index, join_method, drop_idx1, drop_idx2)

	# store recommendation to csv
	rec_result.to_csv(store_path, index=False)

	return rec_result


def mapping(melts, rec_product_name, raw_df, choco_index, join_method, drop_idx1, drop_idx2):
	""" mapping chocolate bars by reference number """
	melts[rec_product_name] = [int(x) for x in melts[rec_product_name]]
	mapped_df = pd.merge(melts, raw_df, left_on=rec_product_name, right_on=choco_index, how=join_method) \
		.drop([drop_idx1, drop_idx2], axis=1)

	return mapped_df


def melting_dataset(df_recs, choco_idx, rank_name, rec_product_name):
	""" melting dataframe and ranking products in dataframe"""
	df_melted = df_recs.melt(id_vars=[choco_idx], var_name=rank_name, value_name=rec_product_name).drop_duplicates()
	df_melted[rank_name] = [int(x.replace('chocolate', '')) for x in df_melted[rank_name]]
	return df_melted
