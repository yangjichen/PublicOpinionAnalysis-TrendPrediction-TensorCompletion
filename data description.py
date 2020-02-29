#coding=utf-8
import pandas as pd
import numpy as np
import util_jichen



path = '/Users/yangjichen/Desktop/项目/舆情分析-tensor/code/jichentest/result0526.csv'
data = pd.read_csv(path)

#删除location是海外和其他的数据390000->320000
data = data[~data['location'].isin(['海外','其他'])]

#print(data['location'].value_counts())
#下面这个变量heat只是为了画热力图
heat =[ (a,b) for a,b in zip(data['location'].value_counts().keys(),data['location'].value_counts().values)]
#下面这个变量只是为了画某一话题在全国分布的热力图
data_hash_tmall = data[data['hashtag']=='天猫双11']
hash_tmall = [(a,b) for a,b in zip(data_hash_tmall['location'].value_counts().keys(),
                                   data_hash_tmall['location'].value_counts().values)]
#下面这个变量是为了画hashtag
hash_value = data['hashtag'].value_counts()
#如果想拿excel打开需要用utf-8-sig编码
#hash_value.to_csv('111.csv',encoding="utf_8_sig")

#选出top50 topic 320000->61000
top_topic = data['hashtag'].value_counts()[0:50].keys()
top_topic_value = data['hashtag'].value_counts()[0:50].values
data = data[data['hashtag'].isin(top_topic)]

#需要将时间划分区间，暂定每小时为1个区间
#time '2018-11-05 14:00:03' -> '2018-11-06 14:16:40'

#为了包含所有时间，区间端点需要小的调整
fanwei=list(range(min(data.time),max(data.time),3600))
fanwei[-1] = max(data.time)
fanwei[0] = fanwei[0]-1

fenzu=pd.cut(data.time,fanwei).cat.codes
fenzu.name = 'fenzu'
#新生成这一列是时间
data = data.join(fenzu)

#调用util里面的函数生成张量
#因为tensor completion代码全部是python 2.7，所以这里需要存储下来，然后使用另外的code进行处理
data_tensor,geo_list,hash_list = util_jichen.build_tensor(data)

np.save('build_tensor.npy',data_tensor)






#可视化效果 热力图
from pyecharts import Map, Geo, Line
attr, value = Geo.cast(heat)
geo = Geo("热力图", "data from weibo", title_color="#fff", title_pos="center", width=1200, height=600,
          background_color='#404a59')
geo.add("热力图", attr, value, visual_range=[0, 10000], type='heatmap', visual_text_color="#fff", symbol_size=16,
        is_visualmap=True)
geo.show_config()
geo.render(path="热力图.html")

#可视化效果 词云
from pyecharts import WordCloud
wordcloud = WordCloud(width=800,height=500)
wordcloud.add('',top_topic,top_topic_value,word_size_range=[20,100])
wordcloud.render(path="词云.html")

#可视化效果 针对不同地区不同话题的区分
attr, value = Geo.cast(hash_tmall)
geo = Geo("双11热力图", "data from weibo", title_color="#fff", title_pos="center", width=1200, height=600,
          background_color='#404a59')
geo.add("热力图", attr, value, visual_range=[0, 80], type='heatmap', visual_text_color="#fff", symbol_size=16,
        is_visualmap=True)
geo.show_config()
geo.render(path="双11热力图.html")

#hashtag衰减比率
line = Line('hashtag')
line.add('amount',hash_value.keys()[0:200],hash_value.values[0:200])
line.render(path = 'hashtag数量衰减图.html')