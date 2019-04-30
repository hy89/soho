import datetime
import json
import time
import pandas as pd
import numpy as np
import requests

from settings import cookies, headers, pagesize


def request(url):
    resp = requests.get(url, headers=headers, cookies=cookies)
    resp = json.loads(resp.content.decode('utf-8'))
    return resp


def first_request():
    print('获取总任务数')
    first_url = 'https://soho.qq.com/api/tasks/me?tabName=done&start=0&limit=10'
    # 请求一次url，获取 总任务数
    resp = request(first_url)
    try:
        total = resp.get('data').get('total')
    except:
        print('请更换cookie后再试')
        total = None
    return total


# 根据total构造请求
def total_request(total):
    print('获取所有任务')
    # tasks返回的是个列表
    url = 'https://soho.qq.com/api/tasks/me?tabName=done&start=0&limit=%s' % total
    resp = request(url)
    tasks = resp.get('data').get('tasks')
    return tasks


def package_request(task):
    package_url = 'https://soho.qq.com/api/tasks/packages?taskId=%s&pageSize=%s&pageNum=1'
    task_id = task.get('taskId')
    package_url = package_url % (task_id, pagesize)
    resp = request(package_url)
    packages = resp.get('data').get('packages')
    for p in packages:
        p['task_id'] = task_id
        p['product_id'] = task.get('productId')
    return packages


def get_data():
    total = first_request()
    if total:
        tasks = total_request(total)
        # 假定每个任务包不超过30个
        print('开始获取package数据')
        all_packages = []
        for task in tasks:
            packages = package_request(task)
            print(packages)
            all_packages.extend(packages)
            time.sleep(1)  # 限制频率，数据量较小，不急于获取
            # break
        print('package数据获取完成')
        return all_packages

    else:
        return


def save2csv(all_packages):
    df = pd.DataFrame(all_packages)
    df.to_csv('./soho-%s.csv' % str(datetime.date.today()))
    # return df


def count_of_coin(df):
    # 计算当前已发放总元宝数
    df_status6 = df[(df.status == 6) & (df.deliverCoin > 0)]  # 取出status=5且coin>0的数据
    coin = df_status6.loc[:, 'deliverCoin'].sum()  # 取出coin列求和即为结果
    return coin


def f(x):
    x = np.round(x, 2)
    if x == 0.85:
        coin = 960
    elif x == 0.9:
        coin = 1280
    elif x == 0.95 or x == 1:
        coin = 1600
    else:
        coin = 0
    return coin


def no_send(df):
    # 计算应发而未发的元宝数量
    # print(df.passRate)
    df_passrate = df[(df.deliverCoin == 0) & (df.passRate >= 0.85) & (df.product_id == 12714588)]
    coins = df_passrate.passRate.map(f)  # map 针对df中的某一列进行操作计算
    return coins


def pass_num(df):
    # print(df.passRate)
    passed = df[((df.status == 6) | (df.status == 5)) & (df.product_id == 12714588) & (df.passRate >= 0.85)]
    passed_num = passed.shape[0]
    no_pass = df[(df.status == 5) & (df.product_id == 12714588) & (df.passRate < 0.85)]
    no_pass_num = no_pass.shape[0]
    # print(passed_num, no_pass_num)
    print('音频--已审通过或已发奖励包数：%s，' % passed_num, '已审未通过包数：%s，' % no_pass_num,
          '通过率：%.2f' % (passed_num / (no_pass_num + passed_num)))


def analysis(df):
    # 根据数据进行分析
    coin = count_of_coin(df)
    print('当前已发放总元宝数：%s；价值RMB %s 元' % (coin, coin / 1000))
    no_send_coins = no_send(df)
    print('音频--已通过但尚未发放奖励包数 %s，合计RMB %s 元' % (no_send_coins.shape[0], no_send_coins.sum() / 1000))
    no_verify_count = df[df.status == 3].shape[0]
    print('音频--当前尚未审核的包数为：%s' % no_verify_count)
    pass_num(df)


def run():
    try:  # 能够读取文件，则读取文件，不能读取则去网络请求获取当天数据，同时将数据保存到csv文件中
        df = pd.read_csv('./soho-%s.csv' % str(datetime.date.today()), index_col=0)
    except:
        all_packages = get_data()
        save2csv(all_packages)  # 保存，再读取
        df = pd.read_csv('./soho-%s.csv' % str(datetime.date.today()), index_col=0)
    print(df)
    analysis(df)


if __name__ == '__main__':
    run()
