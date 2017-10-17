# -*- coding: utf-8 -*-
# @Author  : Mi
# @Function: get the info deeplearn need

'''

    文档说明

    获取一些深度学习需要的数据

'''

import csv
from malldata import getMallData


'''get info'''

def mall_dataGet(mall_name):
    mall_data, mall_shop_id = getMallData(mall_name)
    return mall_data, mall_shop_id


def bssidGet(mall_data, mall_shop_id, mall_name):
    # bssid list
    bssid = []
    bssid_num = 0
    for shop in mall_shop_id[mall_name]:
        bssid_set = set(mall_data[mall_name][shop]['wifiinfo'][0])
        bssid = bssid + (list(bssid_set))
        bssid_num = bssid_num + mall_data[mall_name][shop]['wifiinfo_bssid_num']

    # shop list
    shop_id = []
    shop_id = mall_shop_id[mall_name]

    # two txt:bssid, shop


'''main'''


def main():
    mall_data, mall_shop_id = mall_dataGet('m_690')
    bssidGet(mall_data, mall_shop_id, 'm_690')



if __name__ =='__main__':
    main()



