# -*- coding: utf-8 -*-
# @Author  : Mi
# @Function: get the info deeplearn need

'''

    文档说明

    获取一些深度学习需要的数据

'''


import csv
from malldata import getMallData
from malldata import bssidFilter
from malldata import bssidFilter_max


'''get info'''

def mall_dataGet(mall_name):
    mall_data, mall_shop_id = getMallData(mall_name)
    return mall_data, mall_shop_id


def bssidGet(mall_data, mall_shop_id, mall_name):
    # bssid list
    bssid = []
    bssid_num = 0

    # get filtered bssid
    filtered = bssidFilter_max(mall_data, mall_name, mall_shop_id, 0.6)

    for shop in mall_shop_id[mall_name]:
        bssid = bssid + filtered[shop]['bssid'].keys()
        bssid_num = bssid_num + len(filtered[shop]['bssid'].keys())

    # 写bssid
    f1 = open(r'../source/bssid_list_m_690.txt', 'w')
    f1.write(str(bssid))
    f1.close()

    f2 = open(r'../source/shop_list_m_690.txt', 'w')
    f2.write(str(mall_shop_id[mall_name]))
    f2.close()


    # 构造每条数据
    shop_num = {}
    # 为每个商店编号
    i = 1
    for shop in mall_shop_id[mall_name]:
        if not shop in shop_num.keys():
            shop_num[shop] = i
            i += 1

    check_shop = {}
    with open(r'../source/train_user_info.csv', 'r') as csvf:
        data = csv.DictReader(csvf)
        bssid_file = open(r'../source/bssid_m_690.txt', 'w')
        for line in data:
            curdata = []
            if line['shop_id'] in mall_shop_id[mall_name]:
                # 用字典来存bssid和对应的强度
                if line['shop_id'] in check_shop.keys():
                    check_shop[line['shop_id']] += 1
                else:
                    check_shop[line['shop_id']] = 1
                wifiinfo = {}
                wifiinfo_str = line['wifi_infos']
                wifiinfo_str = wifiinfo_str.split(';')

                for x in wifiinfo_str:
                    x = x.split('|')
                    wifiinfo[x[0]] = x[1]
                for item in bssid:
                    if item in wifiinfo.keys():
                        curdata.append(int(wifiinfo[item]))
                    else:
                        curdata.append(0)

                curdata.append(shop_num[line['shop_id']])

                for item in curdata:
                    bssid_file.write(str(item) + ' ')
                bssid_file.write('\n')

        bssid_file.close()
        a = 1




'''main'''


def main():
    mall_data, mall_shop_id = mall_dataGet('m_690')
    bssidGet(mall_data, mall_shop_id, 'm_690')



if __name__ =='__main__':
    main()



