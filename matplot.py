# @Time    : 2019/5/19 15:41
# @Author  : heyin
# 绘图
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt

def timestamp2date(timestamp):
    """
    时间戳转换为日期
    :param timestamp: 时间戳，int类型
    :return: 日期字符串，如 2019-05-19
    """
    ltime = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d", ltime)


def everyday_tasks():
    """每天做的任务数量"""
    try:
        df = pd.read_csv('./soho-%s.csv' % str(datetime.date.today()), index_col=0)
    except:
        print('文件打开错误')
        return
    # 取出提交时间
    submitDate = df['submitDate']
    # 取秒和取整
    submitDate = submitDate.map(lambda x: int(x/1000))
    # print(submitDate)
    date = submitDate.map(timestamp2date)
    # 以日期分组统计每天的个数
    juhe = date.groupby(date).count()
    print(type(juhe))
    print(juhe.index)
    print(juhe.values)
    plt.plot(juhe.index, juhe.values)
    plt.xticks(juhe.index, rotation=90)
    plt.show()


if __name__ == '__main__':
    # print(timestamp2date(1558240185))
    everyday_tasks()