# -*- coding: utf-8 -*-
# @Author:   Mi
# @Funciong: get the mall number


import csv


'''write txt'''


def writeTxt_mallnumber(data,mallnumber):
    f = open('../source/mall_shop_number.txt', 'w')
    f.write('total mall number: ' + str(mallnumber) + '\n')
    f.write('\n')
    f.write('mall_id  ' + 'shopnumber' + '\n')
    for mallname, shopnumber in data.items():
        f.write(mallname + ':  ' + str(shopnumber) + '\n')
    f.close()


'''get the mall number'''


# read the train_shop_info.csv
def readCsvShop():
    with open('../source/train_shop_info.csv', 'r') as f:
        data = csv.reader(f)

        # 每个mall_id-列表
        mall_id_list = []

        # 每个mall对应的shop数量-字典
        mall_shopnumber = {}

        # mall m_690 的商铺id-字典
        mall_shop_id = {'m_690': []}

        # 总的店铺数
        shop_total = 0

        for line in data:

            if line[-1] == 'mall_id':
                continue

            mall_name = line[-1]
            shop_id = line[0]

            if mall_name in mall_shopnumber.keys():
                mall_shopnumber[mall_name] = 1 + mall_shopnumber[mall_name]
            else:
                mall_shopnumber[mall_name] = 1

            if mall_name == 'm_690':
                mall_shop_id['m_690'].append(shop_id)

            mall_id_list.append(line[-1])

        for key in mall_shopnumber.keys():
            shop_total = mall_shopnumber[key] + shop_total

        mall_id = set(mall_id_list)
    print 'total mall number: ' +str(len(mall_id))
    print 'total shop number: ' + str(shop_total)
    print mall_shop_id
    return mall_shopnumber, len(mall_id), mall_shop_id


def readCvsUser(mallshop_id):
    print len(mallshop_id['m_690'])
    with open('../source/train_user_info.csv') as csvf:
        user_info = csv.DictReader(csvf)

        i = 0

        # for line in user_info:
        #     print line
        #     i += 1
        #     if i > 10:
        #         break

        # wifiinfo in mall: m_690
        wifiinfo_str = ''
        wifiinfo = []

        # for line in user_info:
        #     if line['shop_id'] in mallshop_id['m_690']:
        #         wifiinfo_str = line['wifi_infos']
        #         wifiinfo_str = wifiinfo_str.split(';')
        #         for bssid in wifiinfo_str:
        #             bssid = bssid.split('|')
        #             if not bssid[0] in wifiinfo:
        #                 wifiinfo.append(bssid[0])
        #                 i += 1
        #                 if i > 2:
        #                     print '\n', wifiinfo
        #                     break
        # print len(wifiinfo)
        # print len(set(wifiinfo))

        j = 0
        wifiinfo_shop = []
        for line in user_info:
            if line['shop_id'] == 's_2871718':
                wifiinfo_shop_str = line['wifi_infos']
                wifiinfo_shop_str = wifiinfo_shop_str.split(';')
                for bssid in wifiinfo_shop_str:
                    bssid = bssid.split('|')
                    if not bssid[0] in wifiinfo_shop:
                        wifiinfo_shop.append(bssid[0])
                # print wifiinfo_shop_str
            # j += 1
            # if j > 10:
            #     break
        print wifiinfo_shop
        print len(wifiinfo_shop), len(set(wifiinfo_shop))


'''main'''


def main():
    shopbumber, mallnumber, mallshop_id = readCsvShop()
    # writeTxt_mallnumber(shopbumber, mallnumber)
    readCvsUser(mallshop_id)


if __name__ == '__main__':
    main()
