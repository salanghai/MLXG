# -*- coding: utf-8 -*-
# @Author:   Mi
# @Funciong: collect the mall data including all info from the train set


'''

     文档说明

     mallnum.py中的其他函数可能有问题，不要使用
     尽量使用malldata.py

     数据格式:字典嵌套
     {'m_690': {'s_123':{'longtitude': [],'latitude':[], 'wifiinfo': [[bssid],[-89],[true\false]],'wifiinfo_bssid_num':69,'time_stamp':[[]]}, 's_234':{},.......}}
     使用参考打印数据

     商铺访问量
     画单个商铺一个月的访问量，查看哪几天访问量大等
     画多个商铺访问量，找寻明星商铺
     画平均访问量，了解商铺受欢迎程度

     过滤数据
     可以根据过滤条件filter_rate来设置过滤范围，例如0.7代表把小于最大访问量70%的bssid过滤
     返回一个字典，包含一个商场所有商店过滤后的bssid值

'''


import csv
import matplotlib.pyplot as plt
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
                time_stamp = []
                time_stamp_str = line['time_stamp']
                time_stamp_str = time_stamp_str.split("-")[1:]
                time_stamp.append(time_stamp_str[0])
                time_stamp_str[1] = time_stamp_str[1].split(' ')
                time_stamp.append(time_stamp_str[1][0])
                time_stamp_str = time_stamp_str[1][1].split(':')
                time_stamp.append(time_stamp_str[0])
                time_stamp.append(time_stamp_str[1])
                # print time_stamp

                # 添加数据到mall中
                curshop = line['shop_id']
                if not curshop in mall[mall_name].keys():
                    mall[mall_name][curshop] = {}
                    mall[mall_name][curshop]['longitude'] = []
                    mall[mall_name][curshop]['latitude'] = []
                    mall[mall_name][curshop]['time_stamp'] = []
                    mall[mall_name][curshop]['time_stamp'].append(time_stamp)

                    # 处理下wifiinfo
                    singnal = wifiinfo[1]
                    wifiinfo[1] = []
                    wifiinfo[1].append(singnal)

                    mall[mall_name][curshop]['wifiinfo'] = wifiinfo
                    mall[mall_name][curshop]['longitude'].append(line['longitude'])
                    mall[mall_name][curshop]['latitude'].append(line['latitude'])

                    # mall[mall_name][curshop]['time_stamp'] = line['time_stamp']
                else:
                    mall[mall_name][curshop]['longitude'].append(line['longitude'])
                    mall[mall_name][curshop]['latitude'].append(line['latitude'])
                    mall[mall_name][curshop]['wifiinfo'][0] = mall[mall_name][curshop]['wifiinfo'][0] + wifiinfo[0]
                    mall[mall_name][curshop]['wifiinfo'][1].append(wifiinfo[1])
                    mall[mall_name][curshop]['wifiinfo'][2] = mall[mall_name][curshop]['wifiinfo'][2] + wifiinfo[2]
                    mall[mall_name][curshop]['time_stamp'].append(time_stamp)

    for shop in mall_shop_id[mall_name]:
        mall[mall_name][shop]['wifiinfo_bssid_num'] = len(set(mall[mall_name][shop]['wifiinfo'][0]))
    return mall, mall_shop_id


'''draw the figure of a shop' visit number'''


def visitNumberFigure_oneshop(mall_name, shop_id, mall_data):
    # 每次画一个图
    x = []
    y = []
    y_dict = {}
    for data in mall_data[mall_name][shop_id]['time_stamp']:
        if data[1] in y_dict.keys():
            y_dict[data[1]] += 1
        else:
            y_dict[data[1]] = 1

    for day, num in y_dict.items():
        x.append(int(day))
        y.append(num)

    fig = plt.figure(1)
    ax1 = fig.add_subplot(111)

    ax1.bar(x, y, 0.2)
    xsticks = range(0, max(x) + 1, 1)
    ax1.set_xticks(xsticks)
    plt.xlabel('days')
    plt.ylabel('visit number')
    print 'total visit number: %d' % len(mall_data[mall_name][shop_id]['time_stamp'])
    plt.show()


'''画多个商店访问量，每行3个，每次三行，一次画出9个商店'''


def visitNumberFigure_multishop(mall_name, mall_data):
    # 每次画多个商店访问量
    x = []
    y = []
    y_dict = {}

    shop_numbers, mall_shop_id = readCsvShop(mall_name)
    shop_list = mall_shop_id[mall_name][0: 9]
    fig2 = plt.figure(2)
    for i in range(0, 9):
        for data in mall_data[mall_name][shop_list[i]]['time_stamp']:
            if data[1] in y_dict.keys():
                y_dict[data[1]] += 1
            else:
                y_dict[data[1]] = 1

        for day, num in y_dict.items():
            x.append(int(day))
            y.append(num)

        ax = fig2.add_subplot(331 + i)
        ax.bar(x, y, 0.2)
        # xticks = range(0, max(x) + 1, 1)
        # ax.set_xticks(xticks)
        plt.xlabel('days')
        plt.ylabel('visit number')
        x = []
        y = []
        y_dict = {}

    plt.show()

'''获取一家商场各家店的平均访问量和最高访问量及时间'''


def visitNumberMeans(mall_name, mall_data):
    # 该商场各家店的平均访问量
    x = []
    y = []
    y_dict = {}
    shopVisitMeans = []
    shop_mostVisitDay = []
    shop_mostVisitDay_num = []
    shop_numbers, mall_shop_id = readCsvShop(mall_name)

    for shop in mall_shop_id[mall_name]:
        for data in mall_data[mall_name][shop]['time_stamp']:
            if data[1] in y_dict.keys():
                y_dict[data[1]] += 1

            else:
                y_dict[data[1]] = 1

        for day, num in y_dict.items():
            x.append(int(day))
            y.append(num)

        shop_mostVisitDay.append(x[y.index(max(y))])
        shop_mostVisitDay_num.append(max(y))

        shopVisitMeans.append(sum(x) / len(y))
        x = []
        y = []
        y_dict = {}

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.bar(range(shop_numbers[mall_name]), shopVisitMeans)
    ax.set_title('shop visit number means')

    with open(r'../source/' + mall_name + '_shop_most_visit_day.csv', 'w') as f:
        writer = csv.writer(f)

        writer.writerow(['shop', 'date', 'mostvisitnum'])
        i = 0
        for shop in mall_shop_id[mall_name]:
            writer.writerow([shop, shop_mostVisitDay[i], shop_mostVisitDay_num[i]])
            i += 1
    plt.show()

'''过滤bssid，每家店铺固定bssid'''


def bssidFilter(mall_data, mall_name, mall_shop_id, filter_rate):
    filterd = {}
    for shop in mall_shop_id[mall_name]:
        filterd[shop] = {}
        filterd[shop]['bssid'] = {}
        filterd[shop]['visit'] = len(mall_data[mall_name][shop]['time_stamp'])

        # count each bssid number
        bssid_num = {}
        for x in mall_data[mall_name][shop]['wifiinfo'][0]:
            if not x in bssid_num.keys():
                bssid_num[x] = 1
            else:
                bssid_num[x] = bssid_num[x] + 1
        for bssid, num in bssid_num.items():
            if num > (len(mall_data[mall_name][shop]['time_stamp']) * filter_rate):
                filterd[shop]['bssid'][bssid] = num
            else:
                pass
    a = 1


'''main'''


def main():
    mall, mall_shop_id = getMallData('m_690')

    # 过滤数据,根据bssid
    bssidFilter(mall, 'm_690', mall_shop_id, 0.5)

    # 画一家商店的访问量
    # visitNumberFigure_oneshop('m_1409', 's_3963602', mall)
    # 画多家商店（一次九个，需要自己调参数）
    visitNumberFigure_multishop('m_690', mall)
    # 画一个商场商店访问平均值和写出访问最多那一天的次数和日期
    # visitNumberMeans('m_1409', mall)

    # 打印数据
    # print 's_2871718 total bssid num', mall['m_1409']['s_2871718']['wifiinfo_bssid_num'], '\n'
    # print 's_2871718 all gps:'
    # print 'lonitude:', mall['m_1409']['s_2871718']['longitude'], '\n'
    # print 'latitude', mall['m_1409']['s_2871718']['latitude']


if __name__ == '__main__':
    main()
