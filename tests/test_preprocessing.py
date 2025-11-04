from ml_date_classifier.preprocessing import extract_dates


def test_extract_simple():
    s = 'Manufacture Date: 12/03/2025\nExpiry Date: 11/03/2027'
    d = extract_dates(s)
    assert '12/03/2025' in d
    assert '11/03/2027' in d