# test_sum_module.py

from test import sum1

def test_sum_positive_numbers():
    assert sum1(3, 4) == 7

def test_sum_negative_and_positive():
    assert sum1(-2, 10) == 8

def test_sum_zeros():
    assert sum1(0, 0) == 0
