import validation


def test_valid_username():
    sample_username = "g_ledesma22"

    assert validation.is_username_format_valid(sample_username) is True


def test_invalid_username_with_special_characters():
    sample_username = "g_ledesma2*"

    assert validation.is_username_format_valid(sample_username) is False


def test_invalid_username_too_long():
    sample_username = "g_ledesmaaaaaaaaaaaaaaaaaaaaa"

    assert validation.is_username_format_valid(sample_username) is False


def test_valid_date():
    sample_date = "20221031 220700"

    assert validation.is_date_format_valid(sample_date) is True


def test_invalid_date_wrong_length():
    sample_date = "221031 220700"

    assert validation.is_date_format_valid(sample_date) is False


def test_invalid_date_contains_non_numeric():
    sample_date = "2022Oc31 2207aa"

    assert validation.is_date_format_valid(sample_date) is False


def test_valid_max_result():
    sample_max_result = "1"

    assert validation.is_max_results_valid(sample_max_result) is True


def test_invalid_max_result():
    sample_max_result = "aaksjldnlkq12eddjn2"

    assert validation.is_max_results_valid(sample_max_result) is False
