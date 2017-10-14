# -*- coding: utf-8 -*-
# @Author:   Mi
# @Funciong: collect the mall data including all info from the train set


'''
     文档说明

     mallnum.py中的其他函数可能有问题，不要使用
     尽量使用malldata.py

     数据格式:字典嵌套，易于查找，没有时间戳
     {'m_690': {'s_123':{'longtitude': [],'latitude':[], 'wifiinfo': [[bssid],[-89],[true\false]],'wifiinfo_bssid_num:69}, 's_234':{},.......}}
     使用参考打印数据

'''


import csv
from mallnum import readCsvShop


'''get the mall data including all info from the train set'''


def getMallData(mall_name):

    # get the mall_shop_num and mall_shop_id
    mall_shop_num, mall_shop_id = readCsvShop(mall_name)

    # open train_user_info.csv and deal with data
    with open('../source/train_user_info.csv') as csvf:
        data = csv.DictReader(csvf)

        # 每个商场一个字典，第一层是店铺名，每个店铺也是一个字典，字典值是经纬度和wifi信息
        # {'m_690': {'s_123':{'longtitude': [],'latitude':[], 'wifiinfo': [[bssid],[-89],[true\false]]}, 's_234':{},.......}}
        mall = {mall_name: {}}

        i = 0
        wifiinfo = [[], [], []]

        for line in data:

            if line['shop_id'] in mall_shop_id[mall_name]:

                # wifiinfo数据处理: wifiinfo = [[bssid], [信号强度], [是否连接]]
                wifiinfo = [[], [], []]
                wifiinfo_str = line['wifi_infos']
                wifiinfo_str = wifiinfo_str.split(';')
                for bssid in wifiinfo_str:
                    bssid = bssid.split('|')
                    wifiinfo[0].append(bssid[0])
                    wifiinfo[1].append(bssid[1])
                    wifiinfo[2].append(bssid[2])

                # 时间戳数据处理

                # 添加数据到mall中
                curshop = line['shop_id']
                if not curshop in mall[mall_name].keys():
                    mall[mall_name][curshop] = {}
                    mall[mall_name][curshop]['longitude'] = []
                    mall[mall_name][curshop]['latitude'] = []
                    mall[mall_name][curshop]['wifiinfo'] = wifiinfo
                    mall[mall_name][curshop]['longitude'].append(line['longitude'])
                    mall[mall_name][curshop]['latitude'].append(line['latitude'])
                    # mall[mall_name][curshop]['time_stamp'] = line['time_stamp']
                else:
                    mall[mall_name][curshop]['longitude'].append(line['longitude'])
                    mall[mall_name][curshop]['latitude'].append(line['latitude'])
                    mall[mall_name][curshop]['wifiinfo'][0] = mall[mall_name][curshop]['wifiinfo'][0] + wifiinfo[0]
                    mall[mall_name][curshop]['wifiinfo'][1] = mall[mall_name][curshop]['wifiinfo'][1] + wifiinfo[1]
                    mall[mall_name][curshop]['wifiinfo'][1] = mall[mall_name][curshop]['wifiinfo'][2] + wifiinfo[2]

    for shop in mall_shop_id[mall_name]:
        mall[mall_name][shop]['wifiinfo_bssid_num'] = len(set(mall[mall_name][shop]['wifiinfo'][0]))
    return mall


'''main'''


def main():
    mall = getMallData('m_1409')

    # 打印数据
    print 's_2871718 total bssid num', mall['m_1409']['s_2871718']['wifiinfo_bssid_num'], '\n'
    print 's_2871718 all gps:'
    print 'lonitude:', mall['m_1409']['s_2871718']['longitude'], '\n'
    print 'latitude', mall['m_1409']['s_2871718']['latitude']


if __name__ == '__main__':
    main()

