"""
common exploration
"""

import pandas as pd
from zipfile import ZipFile


def show_unique_columns(data):
    for col in data.columns:
        print('【data.' + col + '.unique().shape】' + '-' * 10)
        print(data[col].unique().shape)


def show_info(data):
    print('【data.info()】' + '-' * 10)
    print(data.info())
    print('【data.head()】' + '-' * 10)
    print(data.head())
    print('【data.shape】' + '-' * 10)
    print(data.shape)
    print('【data.describe()】' + '-' * 10)
    print(data.describe())
    print('【data.isnull().sum()】' + '-' * 10)
    print(data.isnull().sum())
    show_unique_columns(data)


def open_zip(zip_filename, filename):
    myzip = ZipFile(zip_filename)
    f = myzip.open(filename)
    data = pd.read_csv(f)
    f.close()
    myzip.close()
    return data


if __name__ == '__main__':
    data = pd.DataFrame({
        'name': ['you', 'me', 'code'],
        'age': [22, 18, 64]
    })
    show_info(data)
