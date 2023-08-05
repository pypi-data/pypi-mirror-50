# -*- encoding: utf-8
"""
推荐系统评估指标
"""
import numpy as np


def mrr(y_pred, y_true):
    """
    Mean Reciprocal Rank (MRR)
    score(buyer)=\sum _{k=1} ^{30} \frac{s(buyer,k)}{k}
    :param y_pred:
    :param y_true:
    :return:
    """
    rank_count = len(y_true)
    index_row, index_col = np.nonzero(y_pred == y_true)
    hit_row, hit_col = np.unique(index_row, return_index=True)
    target_n = index_col[hit_col] + 1
    return np.sum(1 / target_n) / rank_count, hit_row, target_n


if __name__ == '__main__':
    predict1 = np.array([['catten', 'cati', 'cats', 'caffe']])
    predict2 = np.array([['torii', 'tori', 'toruses', 'tori']])
    predict3 = np.array([['viruses', 'virii', 'viri', 'viruses']])
    predict4 = np.array([['viruses', 'virii', 'viri', 'viruses']])
    y_pred = np.concatenate((predict1, predict2, predict3, predict4), axis=0)
    print(y_pred)

    y_true = np.array([['cats'], ['tori'], ['hello'], ['viruses']])
    print(y_true)

    print(mrr(y_pred, y_true))
