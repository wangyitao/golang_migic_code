import requests
import datetime

from pyquery import PyQuery as pq


filename = 'bbb.txt'
# url = "http://fund.eastmoney.com/fundhot8.html"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
# }
# res = requests.get(url, headers=headers)
# res.encoding = res.apparent_encoding
# doc = pq(res.text)
# # print(doc('body > div:nth-child(8) > table > tbody '))
# items = doc('.div-tb')
# foundDic = {}
# for item in items.items():
#     print('#################')
#     datas = item.find('tr')
#     for data in datas.items():
#         foundName = data.find('.fname').text()
#         persent = data.find('.num').text().strip().split(' ')
#         if len(persent) > 1:
#             persent = [persent[1]]
#         # print(foundName, persent)
#         if foundName.strip() and foundName not in foundDic.keys():
#             f = float(persent[0].strip().replace('%', ''))
#             if f > 40:
#                 foundDic[foundName] = f
# print(foundDic)
# with open(filename, 'a', encoding='utf8') as f:
#     res = sorted(foundDic.items(), key=lambda d: d[1], reverse=True)
#     f.write(
#         '###############################买入人数较多#####################################\n')
#     for r in res:
#         print(r)
#         f.write(str(r) + '\n')

# # 指数型

types = ['zs', 'gp', 'hh']
base_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft={}&rs=&gs=0&sc=qjzf&st=desc&sd={}&ed={}&es=0&qdii=&pi=1&pn=50'
# url2 = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=zs&rs=&gs=0&sc=qjzf&st=desc&sd={}&ed={}&es=0&qdii=&pi=1&pn=50&dx=0&v=0.4450390071011794'
# url3 = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=gp&rs=&gs=0&sc=qjzf&st=desc&sd={}&ed={}&es=0&qdii=&pi=1&pn=50&dx=0&v=0.5034547738743769'
# url4 = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=hh&rs=&gs=0&sc=qjzf&st=desc&sd={}&ed={}&es=0&qdii=&pi=1&pn=50&dx=0&v=0.060176775502043256'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
jijingDic = {}

end = 410
step = 15
today = datetime.datetime.now()
yestoday = today - datetime.timedelta(days=1)
# for typ in types:
#     i = 20
#     while i <= end:
#         print(i+'@@@@@')
#         startDay = yestoday - datetime.timedelta(days=i)
#         url = base_url.format(typ, startDay.date(), yestoday.date())
#         res = requests.get(url, headers=headers)
#         res.encoding = res.apparent_encoding
#         datas = res.text.split('[')[1].split(']')[
#             0].strip('"').split('","')[:10]
#         for data in datas:
#             aaa = data.split(',')
#             num = aaa[0]
#             name = aaa[1]
#             persent = aaa[3]
#             print(name, persent)
#             if name not in jijingDic.keys():
#                 jijingDic[name] = [
#                     (float(persent)/float(i), name, persent, num)]
#             else:
#                 jijingDic[name].append(
#                     (float(persent)/float(i), name, persent, num))
#         i += step


# with open(filename, 'a', encoding='utf8') as f:
#     result = {}
#     for k, v in jijingDic.items():
#         sum = 0
#         for dd in v:
#             sum += dd[0]
#         result[k] = (sum, sum/len(v), v[-1], len(v))
#     res = sorted(result.items(), key=lambda d: d[1][0], reverse=True)
#     f.write(
#         '################################总计算值排放###################################\n')
#     for r in res:
#         print(r)
#         f.write(str(r) + '\n')
#     f.write(
#         '###############################总计算值前十#####################################\n')
#     for r in res[:10]:
#         print(r)
#         f.write(str(r) + '\n')

#     res = sorted(result.items(), key=lambda d: d[1][1], reverse=True)
#     f.write(
#         '###############################平均每日收益#####################################\n')
#     for r in res:
#         print(r)
#         f.write(str(r) + '\n')
#     f.write(
#         '###############################平均每日收益前十#####################################\n')
#     for r in res[:10]:
#         print(r)
#         f.write(str(r) + '\n')

jijingDic2 = {}
for typ in types:
    i = 20
    endDay = yestoday
    while i <= end:
        print(i+'@@@@@')
        startDay = endDay - datetime.timedelta(days=step)
        url = base_url.format(typ, startDay.date(), endDay.date())
        endDay = startDay
        res = requests.get(url, headers=headers)
        res.encoding = res.apparent_encoding
        datas = res.text.split('[')[1].split(']')[
            0].strip('"').split('","')[:10]
        for data in datas:
            aaa = data.split(',')
            num = aaa[0]
            name = aaa[1]
            persent = aaa[3]
            print(name, persent)
            if name not in jijingDic2.keys():
                jijingDic2[name] = [
                    (float(persent)/float(i), name, persent, num)]
            else:
                jijingDic2[name].append(
                    (float(persent)/float(i), name, persent, num))
        i += step

with open(filename, 'a', encoding='utf8') as f:
    result = {}
    for k, v in jijingDic2.items():
        sum = 0
        for dd in v:
            sum += dd[0]
        result[k] = (sum, sum/len(v), v[-1], len(v))

    res = sorted(result.items(), key=lambda d: d[1][1], reverse=True)
    f.write(
        '###############################第三种计算方式平均每日收益#####################################\n')
    for r in res:
        print(r)
        f.write(str(r) + '\n')
    f.write(
        '###############################第三种计算方式平均每日收益前十#####################################\n')
    for r in res[:10]:
        print(r)
        f.write(str(r) + '\n')
