import pandas as pd
import pytest

from src.modeling import get_userinput, formatting_preds, melting_dataset, mapping


def test_get_userinput():
    """test if get_userinput() can accurately format user input"""
    inputs = [72.0, 4.5, "Yes", 'No', "Yes", 'No',"Yes", "Yes", 'No']
    features = ['index', 'cocoa_percent', 'rating', 'beans', 'cocoa_butter', 'vanilla', 'lecithin', 'salt', 'sugar',
                'sweetener_without_sugar']

    df_true = pd.DataFrame([['999999', 72.0, 4.5, 1, 0, 1, 0, 1, 1, 0]],columns=features)

    df_test = get_userinput(*inputs, input_cols=features, preset_index='999999', replace_dict={'No': 0, 'Yes': 1})

    pd.testing.assert_frame_equal(df_true, df_test)


def test_get_userinput_unhappy():
    """test if dataframe is not provided to get_userinput()"""
    inputs = 'not a list'
    features = ['index', 'cocoa_percent', 'rating', 'beans', 'cocoa_butter', 'vanilla', 'lecithin', 'salt', 'sugar',
                'sweetener_without_sugar']

    with pytest.raises(TypeError):
        get_userinput(*inputs, input_cols=features, preset_index='999999', replace_dict={'No': 0, 'Yes': 1})


def test_formatting_preds():
    """test if formatting_preds() can accurately organize the prediction and generate recommendation table"""
    features = ['index', 'cocoa_percent', 'rating', 'beans', 'cocoa_butter', 'vanilla','lecithin', 'salt', 'sugar',
                'sweetener_without_sugar', 'cluster_label']

    web_display_vars = ['index', 'company', 'specific_bean_origin_or_bar_name', 'cocoa_percent', 'rating', 'first_taste',
                        'second_taste']

    df_in = pd.DataFrame([[0, 76.0, 3.75, 1, 1, 0, 0, 0, 1, 0, 2],
                          [1, 76.0, 3.5, 1, 1, 0, 0, 0, 1, 0, 2],
                          [2, 76.0, 3.25, 1, 1, 0, 0, 0, 1, 0, 8],
                          [3, 63.0, 3.75, 1, 1, 0, 1, 0, 1, 0, 8],
                          [4, 70.0, 3.5, 1, 1, 0, 1, 0, 1, 0, 5],
                          [5, 70.0, 4.0, 1, 1, 0, 1, 0, 1, 0, 5],
                          ['999999', 72.0, 4.5, 1, 0, 1, 0, 1, 1, 0, 2]], columns=features)

    df_web_display = pd.DataFrame([[0, '5150', 'Bejofo Estate, batch 1', 76.0, 3.75, 'cocoa', 'blackberry'],
                                  [1, '5150', 'Zorzal, batch 1', 76.0, 3.5, 'cocoa', 'vegetal'],
                                  [2, '5150', 'Kokoa Kamili, batch 1', 76.0, 3.25, 'rich cocoa', 'fatty'],
                                  [3, 'A. Morin', 'Peru', 63.0, 3.75, 'fruity', 'melon'],
                                  [4, 'A. Morin', 'Bolivia', 70.0, 3.5, 'vegetal', 'nutty'],
                                  [5, 'A. Morin', 'Chuao', 70.0, 4.0, 'oily', 'nut']], columns=web_display_vars)

    df_test = formatting_preds(df_in, df_web_display, features, 2, 'test_formatting_preds.csv')

    df_true = pd.DataFrame([[1, 1, '5150', 'Zorzal, batch 1', 76.0, 3.5, 'cocoa', 'vegetal'],
                            [2, 0, '5150', 'Bejofo Estate, batch 1', 76.0, 3.75, 'cocoa', 'blackberry']],
                           columns=['rank', 'chocolate_bar', 'company', 'specific_bean_origin_or_bar_name',
                           'cocoa_percent', 'rating', 'first_taste', 'second_taste'])

    pd.testing.assert_frame_equal(df_true, df_test)


def test_formatting_preds_unhappy():
    """test if dataframe is not provided to formatting_preds()"""
    df_in = "not a df"
    df_web_display = "not a df either"

    features = ['index', 'cocoa_percent', 'rating', 'beans', 'cocoa_butter', 'vanilla', 'lecithin', 'salt', 'sugar',
                'sweetener_without_sugar', 'cluster_label']

    with pytest.raises(TypeError):
        formatting_preds(df_in, df_web_display, features, 2, 'test_formatting_preds.csv')


def test_melting_dataset():
    """test if melting_dataset() can accurately melt the dataframe"""
    df_in = pd.DataFrame([[999999, 1, 0]], columns=['index', 'chocolate1', 'chocolate2'])

    df_test = melting_dataset(df_in, choco_idx='index', rank_name='rank', rec_product_name='chocolate_bar')

    df_true = pd.DataFrame([[999999, 1, 1], [999999, 2, 0]], columns=['index', 'rank', 'chocolate_bar'])

    pd.testing.assert_frame_equal(df_true, df_test)


def test_melting_dataset_unhappy():
    """test if dataframe is not provided to melting_dataset()"""
    df_in = "not a df"
    with pytest.raises(AttributeError):
        melting_dataset(df_in, choco_idx='index', rank_name='rank', rec_product_name='chocolate_bar')


def test_mapping():
    """test if mapping() can accurately map chocolate bar indexes with the feature dataframe"""
    df_in = pd.DataFrame([[999999, 1, 1], [999999, 2, 0]], columns=['index', 'rank', 'chocolate_bar'])

    df_true = pd.DataFrame([[1, 1, '5150', 'Zorzal, batch 1', 76.0, 3.5, 'cocoa', 'vegetal'],
                            [2, 0, '5150', 'Bejofo Estate, batch 1', 76.0, 3.75, 'cocoa','blackberry']],
                           columns=['rank', 'chocolate_bar', 'company', 'specific_bean_origin_or_bar_name',
                           'cocoa_percent', 'rating', 'first_taste', 'second_taste'])

    df_for_merging = pd.DataFrame([[0, '5150', 'Bejofo Estate, batch 1', 76.0, 3.75, 'cocoa','blackberry'],
                            [1, '5150', 'Zorzal, batch 1', 76.0, 3.5, 'cocoa', 'vegetal'],
                            [2, '5150', 'Kokoa Kamili, batch 1', 76.0, 3.25, 'rich cocoa','fatty']],
                          columns=['index', 'company', 'specific_bean_origin_or_bar_name', 'cocoa_percent', 'rating',
                                   'first_taste', 'second_taste'])

    df_test = mapping(df_in, rec_product_name='chocolate_bar', raw_df=df_for_merging, choco_index='index',
                      join_method='inner', drop_idx1='index_x', drop_idx2='index_y')

    pd.testing.assert_frame_equal(df_true, df_test)


def test_mapping_unhappy():
    """test if dataframe is not provided to mapping()"""
    df_in = "not a df"
    df_for_merging = "not a df either"

    with pytest.raises(TypeError):
        mapping(df_in, rec_product_name='chocolate_bar', raw_df=df_for_merging, choco_index='index',join_method='inner',
                drop_idx1='index_x', drop_idx2='index_y')