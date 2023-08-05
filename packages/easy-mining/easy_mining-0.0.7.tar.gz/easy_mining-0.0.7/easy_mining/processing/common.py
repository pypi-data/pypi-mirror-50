# -*- encoding: utf-8
"""
数据处理常用模块
"""


def select_columns(data, col=[], dtype_dict=None):
    """
    选择列并指定类型
    :param data:
    :param col:
    :param dtype_dict:
    :return:
    """
    memory = data.memory_usage().sum() / 1024 ** 2
    print('Before memory usage of properties dataframe is :', memory, " MB")

    data = data[col]
    if dtype_dict is not None:
        data = data.astype(dtype_dict)

    memory = data.memory_usage().sum() / 1024 ** 2
    print('After memory usage of properties dataframe is :', memory, " MB")
    return data
