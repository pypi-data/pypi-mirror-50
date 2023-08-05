# -*- encoding: utf-8
from easy_mining.processing import date
import pandas as pd


def test_date_split():
    data = pd.DataFrame({
        'name': ['you', 'me', 'code'],
        'time': ['2018-01-10 11:23:44', '2017-02-06 1:55:12', '2019-03-20 23:01:23']
    })
    data = date.date_split(data, 'time')
    assert data['day'] is not None, "test failed"
