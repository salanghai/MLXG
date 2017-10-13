# -*- coding: utf-8 -*-
# @Author:   Mi
# @Funciong: get the mall number


import csv


'''write txt'''
def writeTxt_mallnumber(data,mallnumber):
    f = open('/home/mjl/MLXG/mlxg/souce/mall_shop_number.txt', 'w')
    f.write('total mall number: ' + str(mallnumber) + '\n')
    f.write('\n')
    f.write('mall_id  ' + 'shopnumber' + '\n')
    for mallname, shopnumber in data.items():
        f.write(mallname + ':  ' + str(shopnumber) + '\n')
    f.close()


'''get the mall number'''

# read the train_shop_info.csv
def readCsvShop():
    with open('/home/mjl/MLXG/mlxg/souce/train_shop_info.csv', 'r') as f:
        data = csv.reader(f)
        mall_id_list = []
        mall_shopnumber = {}
        mall_shop_id = {'m_690': []}
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
    print len(mall_id)
    print shop_total
    print mall_shop_id
    return mall_shopnumber, len(mall_id), mall_shop_id


def readCvsUser(mallshop_id):
    with open('/home/mjl/MLXG/mlxg/souce/train_user_info.csv') as csvf:
        user_info = csv.DictReader(csvf)

        i = 0

        for line in user_info:
            print line
            i += 1
            if i > 10:
                break

        for line in user_info:
            if line['shop_id'] in mallshop_id:
                break



'''main'''

def main():
    shopbumber, mallnumber, mallshop_id = readCsvShop()
    writeTxt_mallnumber(shopbumber, mallnumber)
    readCvsUser(mallshop_id)


if __name__ == '__main__':
    main()
