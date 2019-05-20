# @Time    : 2019/5/19 15:41
# @Author  : heyin
# 绘图
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
from example.commons import Faker
from pyecharts.charts import Bar, Line
from pyecharts import options as opts


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
    submitDate = submitDate.map(lambda x: int(x / 1000))
    # print(submitDate)
    date = submitDate.map(timestamp2date)
    # 以日期分组统计每天的个数
    juhe = date.groupby(date).count()
    # print(juhe.shape[0])
    # plt.figure(figsize=(20, 8))
    # plt.plot(juhe.index, juhe.values)
    # for a, b in zip(juhe.index, juhe.values):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=16)
    # plt.xticks(juhe.index, rotation=90)
    # plt.show()

    bar = (
        Bar()
            .add_xaxis(list(juhe.index))
            .add_yaxis("任务量", [int(i) for i in juhe.values])
            .set_global_opts(title_opts=opts.TitleOpts(title="任务量统计", subtitle="天数：%s"%juhe.shape[0]))
        # 或者直接使用字典参数
        # .set_global_opts(title_opts={"text": "主标题", "subtext": "副标题"})
    )
    bar.render()


if __name__ == '__main__':
    # print(timestamp2date(1558240185))
    everyday_tasks()
    # line_base().render()
