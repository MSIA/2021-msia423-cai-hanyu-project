import pandas as pd
import pytest

from src.clean_data import clean, standardization


def test_clean():
    """test if clean() can accurately convery binary features into numeric ones"""
    features = ['index', 'company', 'specific_bean_origin_or_bar_name', 'cocoa_percent', 'rating', 'beans',
                'cocoa_butter', 'vanilla', 'lecithin', 'salt', 'sugar', 'sweetener_without_sugar', 'first_taste',
                'second_taste']

    df_in = pd.DataFrame([[1, "msia company", "evanston", 72.0, 4.5, "no bean", "no cocoa_butter", "vanilla",
                           "no lecithin", "salt", 'sugar', 'no sweetener_without_sugar', 'roasty', 'strong'],
                          [2, "avc company", "zoom", 55.9, 4, "bean", "no cocoa_butter", "no vanilla", "no lecithin",
                           "no salt", 'sugar', 'no sweetener_without_sugar', 'sweet', 'milk'],
                          [3, "hanyu company", "ridge ave", 78.2, 3.5, "no bean", "no cocoa_butter", "vanilla",
                           "no lecithin", "salt", 'sugar', 'sweetener_without_sugar', 'coconut', 'fruity']]
                         , columns=features)

    df_true = pd.DataFrame([[1, "msia company", "evanston", 72.0, 4.5, 0, 0, 1, 0, 1, 1, 0,'roasty','strong'],
                          [2, "avc company", "zoom", 55.9, 4, 1, 0, 0, 0, 0, 1, 0, 'sweet','milk'],
                          [3, "hanyu company", "ridge ave", 78.2, 3.5, 0, 0, 1, 0, 1, 1, 1, 'coconut','fruity']]
                         , columns=features)

    df_test = clean(df_in, enc_features=['beans','cocoa_butter', 'vanilla', 'lecithin', 'salt', 'sugar',
                                         'sweetener_without_sugar'],
                    store_path='data/clean_data.csv', clean_features=features, binary_word="no")

    pd.testing.assert_frame_equal(df_true, df_test)


def test_clean_unhappy():
    """test if dataframe is not provided to clean()"""
    df_in = "not a df"
    features = ['index', 'company', 'specific_bean_origin_or_bar_name', 'cocoa_percent', 'rating', 'beans',
                'cocoa_butter', 'vanilla', 'lecithin', 'salt', 'sugar', 'sweetener_without_sugar', 'first_taste',
                'second_taste']

    with pytest.raises(TypeError):
        clean(df_in, enc_features=['beans', 'cocoa_butter', 'vanilla', 'lecithin', 'salt', 'sugar',
                                   'sweetener_without_sugar'],
              store_path='data/clean_data.csv', clean_features=features, binary_word="no")


def test_standardization():
    """test if standardization() can accurately standardize input dataframe"""
    features = ['feature1', 'feature2', 'feature3']
    df_in = pd.DataFrame([[1, 1, 2], [3, 4, 3], [2, 2, 2]], columns=features)
    
    df_true = pd.DataFrame([[-1.224744871391589, -1.0690449676496978, -0.7071067811865478],
                            [1.224744871391589, 1.3363062095621219, 1.4142135623730947],
                            [0.0, -0.2672612419124245, -0.7071067811865478]], columns=features)

    df_test = standardization(df_in, features)

    pd.testing.assert_frame_equal(df_true, df_test)


def test_standardization_unhappy():
    """test if dataframe is not provided to standardization()"""
    features = ['feature1', 'feature2', 'feature3']
    df_in = "not a df and thus doesn't have the copy attribute"
    
    with pytest.raises(AttributeError):
        standardization(df_in, features)
