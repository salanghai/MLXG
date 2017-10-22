# -*- coding: utf-8 -*-
# @Author:   Mi
# @Funciong: model


import csv
import time
import xgboost as xgb
import numpy as np
import pandas as pd
from preprocess.Processforxgboost import mall
from sklearn.cross_validation import train_test_split

# 记录运行时间
start_time = time.clock()


class mall_model(mall):
    def model(self):
        data = pd.read_csv(r'../model_use/filtered_bssid_' + self.name +'.csv')
        label = data['label']
        num_class = len(set(label)) + 1
        train = data.drop(['label'], axis = 1)
        train_x, test_x, train_y, test_y = train_test_split(train, label, test_size=0.2, random_state=1)

        xgb_train = xgb.DMatrix(train_x, label=train_y)
        xgb_test = xgb.DMatrix(test_x, label=test_y)

        params = {
            'booster': 'gbtree',
            'objective': 'multi:softmax', # 多分类问题
            'num_class': num_class,       # 类别数
            'gamma': 0.1,                 # 用于是否控制后剪枝，一般0.1,0.2
            'max_depth': 10,              # 最大树的深度 越深越容易过拟合
            'lambda': 2,                  # 控制模型复杂度的权重值的L2正则化参数，越大越不容易过拟合
            'silent': 1,                  # 运行时是否显示信息0：显示
            'eta': 0.007,                 # 学习率
        }

        plst = list(params.items())
        num_rounds = 10
        watchlist = [(xgb_train, 'train'), (xgb_test, 'eval')]

        # 训练并保存
        model = xgb.train(params, xgb_train, num_rounds, watchlist)
        model.save_model(r'../model_save/' + self.name + '.model')

        a = 1




'''main'''


def main():
    mall_name = 'm_2224'
    m_2224 = mall_model(mall_name)
    m_2224.run()
    m_2224.model()
    cost_time = time.clock() - start_time
    print cost_time
    a = 1


if __name__ == '__main__':
    main()
