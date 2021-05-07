import pytest

from src.s3 import parse_s3


def test_parse_s3():
    s3path = "s3://example_bucket/example_file.csv"
    tuple_true = ("example_bucket", "example_file.csv")
    tuple_test = parse_s3(s3path)
    assert tuple_test == tuple_true


def test_parse_s3_invalid_path():
    s3path = "justrandompath"
    with pytest.raises(AttributeError):
        parse_s3(s3path)
