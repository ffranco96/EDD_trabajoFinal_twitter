import os
import pytest

import menu_options
import util


@pytest.fixture
def sample_json():
    return util.load_tweets(os.getcwd() + "/test_files/test6.json")


def test_filter_tweets_no_params(sample_json):
    # Se devuelve la lista entera
    filtered_results = menu_options.filter_tweets(sample_json)

    assert sample_json == filtered_results
