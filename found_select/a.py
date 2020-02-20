import threading
from apscheduler.schedulers.blocking import BlockingScheduler  # pip install apscheduler
import requests  # pip install requests
import datetime
import json
import os
from pyquery import PyQuery as pq  # pip install pyquery
import itchat  # pip install itchat
import time


json_file = 'main.json'
today = datetime.datetime.now()


def select_found():
    global json_file, today
    jijingDic = {}

    end = 410
    step = 15
    limit = 10
    select_limit = 10

    yestoday = today - datetime.timedelta(days=1)
    money = 1000
    filename = str(datetime.datetime.now()).split('.')[0].replace(
        ' ', '').replace('-', '').replace(':', '').strip()+'bbb.txt'
    url = "http://fund.eastmoney.com/fundhot8.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    doc = pq(res.text)
    # print(doc('body > div:nth-child(8) > table > tbody '))
    items = doc('.div-tb')
    foundDic = {}
    for item in items.items():
        # print('#################')
        datas = item.find('tr')
        for data in datas.items():
            foundName = data.find('.fname').text()
            persent = data.find('.num').text().strip().split(' ')
            if len(persent) > 1:
                persent = [persent[1]]
            # print(foundName, persent)
            if foundName.strip() and foundName not in foundDic.keys():
                f = float(persent[0].strip().replace('%', ''))
                if f > 40:
                    foundDic[foundName] = f
    # print(foundDic)
    with open(filename, 'a', encoding='utf8') as f:
        res = sorted(foundDic.items(), key=lambda d: d[1], reverse=True)
        f.write(
            '###############################买入人数较多#####################################\n')
        for r in res:
            # print(r)
            f.write(str(r) + '\n')

    # # 指数型

    types = ['zs', 'gp', 'hh']
    base_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft={}&rs=&gs=0&sc=qjzf&st=desc&sd={}&ed={}&es=0&qdii=&pi=1&pn=50'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }

    for typ in types:
        i = 20
        while i <= end:
            # print(i, '@@@@@')
            startDay = yestoday - datetime.timedelta(days=i)
            url = base_url.format(typ, startDay.date(), yestoday.date())
            res = requests.get(url, headers=headers)
            res.encoding = res.apparent_encoding
            datas = res.text.split('[')[1].split(']')[
                0].strip('"').split('","')[:limit]
            for data in datas:
                aaa = data.split(',')
                num = aaa[0]
                name = aaa[1]
                persent = aaa[3]
                # print(name, persent)
                if name not in jijingDic.keys():
                    jijingDic[name] = [
                        (float(persent)/float(i), name, persent, num, typ)]
                else:
                    jijingDic[name].append(
                        (float(persent)/float(i), name, persent, num, typ))
            i += step

    with open(filename, 'a', encoding='utf8') as f:
        result = {}
        for k, v in jijingDic.items():
            sum = 0
            for dd in v:
                sum += dd[0]
            result[k] = (sum, sum/len(v), v[-1], len(v))
        res = sorted(result.items(), key=lambda d: d[1][0], reverse=True)
        f.write(
            '################################总计算值排放###################################\n')
        for r in res:
            # print(r)
            f.write(str(r) + '\n')
        f.write(
            '###############################总计算值前十#####################################\n')
        for r in res[:select_limit]:
            # print(r)
            f.write(str(r) + '\n')
        f.write(
            '###############################购买推荐前十#####################################\n')
        ddic = {}
        ssum = 0
        rs = []
        rs_dic = {}
        for r in res[:select_limit]:
            ddic[r[0]] = (r[-1][-1], r[1][2][-2])
            ssum += r[-1][-1]
        for k, v in ddic.items():
            r = (v[1], k, v[0] / ssum * money)
            rs.append(r)
            rs_dic[r[0]] = r
            # print(r)
            f.write(str(r) + '\n')

        data = {'buy': {}, 'sale': {}}
        for rr in rs:
            # print(rr)
            data['buy'][rr[0]] = rr[1]
        # print(data)

        if not os.path.exists(json_file):
            pass
        else:
            with open(json_file, 'r', encoding='utf8') as f:
                load_dict = json.load(f)
                # print("读取出的数据为:{}".format(load_dict))
                buy = load_dict['buy']
                sale = load_dict['sale']
                for key, value in buy.items():
                    if key not in data.keys():
                        data['sale'][key] = value
        buy = data['buy']
        for k, v in buy.items():
            buy[k] = (v, round(rs_dic[k][2], 2))
        sale = data['sale']
        buy_kk = buy.keys()
        sale_kk = sale.keys()
        for k in list(sale_kk):
            if k in list(buy_kk):
                data['sale'].pop(k)
        data['buy'] = buy
        data['tiantian'] = foundDic
        data['date'] = str(today.date())
        with open(json_file, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)

        buy = data['buy']
        sale = data['sale']
        # print('买入规则：如果上证指数在当天14.40的时候下跌，可以买入，否则可以卖出，如果上证指数在2900以下，不建议卖出，在3050以上不建议买入')
        # print('以下基金可以买入(以1000元为基准)：')
        # for key, v in buy.items():
        #     print('{} {} {}元'.format(rs_dic[key][0],
        #                              rs_dic[key][1], round(rs_dic[key][2], 2)))
        # print('如果之前按照推荐买入的，以下现在不推荐了，建议找机会卖出：')
        # for key, v in sale.items():
        #     print('{} {}'.format(key, v))
        return buy, sale


# select_found()
def get_data():
    global json_file, today
    if not os.path.exists(json_file):
        select_found()
        time.sleep(1)

    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf8') as f:
            load_dict = json.load(f)
            # print("读取出的数据为:{}".format(load_dict))
            date = datetime.datetime.strptime(
                load_dict['date'], '%Y-%m-%d').date()
            if (today.date() - date).days > 7:
                select_found()
                time.sleep(1)
            else:
                return load_dict['buy'], load_dict['sale'], load_dict['tiantian']

    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf8') as f:
            load_dict = json.load(f)
            # print("读取出的数据为:{}".format(load_dict))
            return load_dict['buy'], load_dict['sale'], load_dict['tiantian']
    else:
        return None


# buy, sale = get_data()
# print(buy, sale)


def get_reply_content():
    try:
        datas = get_data()
    except Exception as e:
        return ''
    if datas != None:
        buy, sale, tiantian = datas
    else:
        return ''
    buy_str = ''
    for k, v in buy.items():
        buy_str += '{} {} {}元\n'.format(k, v[0], v[1])
    sele_str = ''
    for k, v in sale.items():
        sele_str += '{} {}\n'.format(k, v[0])
    tiantian_str = ''
    for k, v in tiantian.items():
        tiantian_str += '{} {}\n'.format(k, v)

    content = '买入规则：如果上证指数在当天14.40的时候下跌，可以买入，否则可以卖出，如果上证指数在2900以下，不建议卖出，在3050以上不建议买入\n以下基金可以买入(以1000元为基准)：\n{}\n如果之前按照推荐买入的，以下现在不推荐了，建议找机会卖出：\n{}\n以下为购买人数较多基金基金：\n{}\n'.format(
        buy_str, sele_str, tiantian_str)
    # print(content)
    return content


# get_reply_content()

# 自动回复
@itchat.msg_register('Text', isGroupChat=False)
def test_reply(msg):
    try:
        content = msg['Content'].strip()  # 获取微信收到的消息
        fromUser = msg['FromUserName']  # 获取发送用户id
        if '基金' == content:
            cons = get_reply_content()
            if msg['ToUserName'] == 'filehelper':
                itchat.send(cons, 'filehelper')  # 发送消息
            else:
                itchat.send(cons, fromUser)  # 发送消息
    except Exception as e:
        with open('run.log', 'a', encoding='utf8') as f:
            f.write(str(e))


class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()
        # 重写run()方法，使它包含线程需要做的工作

    def run(self):
        # 设置定时任务，每隔6天更新一次
        sched = BlockingScheduler()
        sched.add_job(get_data, 'interval', days=6,
                      hours=0, minutes=0, seconds=0)
        sched.start()


# 启动的时候获取一次数据
get_data()

# 开启定时获取
mythead = MyThread()
mythead.start()

# 启动微信
itchat.auto_login(enableCmdQR=2)  # 登录微信  如果不想每次登录都扫码添加参数hotReload=True
itchat.run()  # 运行
mythead.join()
