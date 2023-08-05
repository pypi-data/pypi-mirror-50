"""
common exploration
"""

import pandas as pd
from zipfile import ZipFile


def show_unique_columns(data):
    for col in data.columns:
        print('【data.' + col + '.unique().shape】\n')
        print(data[col].unique().shape)


def show_info(data):
    print('【data.info()】\n', data.info())
    print('【data.head()】\n', data.head())
    print('【data.shape】\n', data.shape)
    print('【data.describe()】\n', data.describe())
    print('【data.isnull().sum()】\n', data.isnull().sum())
    show_unique_columns(data)
    return data.info


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
