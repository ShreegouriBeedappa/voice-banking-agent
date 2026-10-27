
from amount_parser import parse_amount


def test_numeric_amount():
    assert parse_amount("500 rupees") == 500


def test_amount_without_currency():
    assert parse_amount("1500") == 1500


def test_amount_with_inr():
    assert parse_amount("250000 INR") == 250000


def test_hinglish_amount():
    assert parse_amount("paanch sau") == 500
    assert parse_amount("dhai sau") == 250
    assert parse_amount("dedh hazaar") == 1500
    assert parse_amount("sawa do lakh") == 225000

def test_other_special_amounts():
    assert parse_amount("dedh sau") == 150
    assert parse_amount("dhai lakh") == 250000
    assert parse_amount("dedh lakh") == 150000
    assert parse_amount("ek lakh") == 100000
