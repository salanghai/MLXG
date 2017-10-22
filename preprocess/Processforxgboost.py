# -*- coding: utf-8 -*-
# @Author:   Mi
# @Funciong: process for xgboost


import csv
from malldata import bssidFilter_max
from malldata import bssidFilter
from malldata import getMallData
from writeCsv import writeBssid


class mall(object):

    def __init__(self, name):
        self.name = name
        self.shop_id = {}
        self.data = {}
        self.filtered = {}

    def dataGet(self):
        self.data, self.shop_id = getMallData(self.name)

    def bssidFilter(self, rate):
        self.filtered = bssidFilter(self.data, self.name, self.shop_id, filter_rate=rate)

    def bssidFilter_max(self, rate):
        self.filtered = bssidFilter_max(self.data, self.name, self.shop_id, filter_rate=rate)

    def writeBssidCsv(self):
        writeBssid(mall_name=self.name, mall_shop_id=self.shop_id, filtered=self.filtered)

    def run(self):
        self.dataGet()
        self.bssidFilter_max(0.9)
        self.writeBssidCsv()

