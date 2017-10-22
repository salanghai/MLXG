# -*- coding: utf-8 -*-
# @Author:   Mi
# @Funciong: write some csv file


import csv


# 构造每条数据
def writeBssid(mall_name, mall_shop_id, filtered):
    # bssid list
    bssid = []
    bssid_num = 0

    for shop in mall_shop_id[mall_name]:
        bssid = bssid + filtered[shop]['bssid'].keys()
        bssid_num = bssid_num + len(filtered[shop]['bssid'].keys())
    shop_num = {}
    # 为每个商店编号
    i = 1
    for shop in mall_shop_id[mall_name]:
        if not shop in shop_num.keys():
            shop_num[shop] = i
            i += 1
    # 写数据
    check_shop = {}
    bssid_file = open(r'../model_use/filtered_bssid_' + mall_name + '.csv', 'w')
    header = []
    for i in range(len(bssid)):
        header.append(str(i))
    header.append('label')
    csvwriter = csv.writer(bssid_file)
    csvwriter.writerow(header)
    with open(r'../source/train_user_info.csv', 'r') as csvf:
        data = csv.DictReader(csvf)
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

                csvwriter.writerow(curdata)
                '''
                for item in curdata:
                    bssid_file.write(str(item) + ' ')
                bssid_file.write('\n')
                '''

        bssid_file.close()