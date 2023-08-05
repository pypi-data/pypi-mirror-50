"""date processing."""
import pandas as pd


def date_split(data, col):
    data[col] = data[col].apply(lambda x: pd.to_datetime(x))
    data['year'] = data[col].dt.year
    data['month'] = data[col].dt.month
    data['day'] = data[col].dt.day
    data['hour'] = data[col].dt.hour
    data['minute'] = data[col].dt.minute
    data['second'] = data[col].dt.second
    return data
