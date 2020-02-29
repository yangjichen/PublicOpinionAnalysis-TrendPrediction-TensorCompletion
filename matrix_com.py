#coding=utf-8
import pandas as pd
import numpy as np
from fancyimpute import KNN, NuclearNormMinimization, IterativeSVD, IterativeImputer, BiScaler

geo_list = np.array(['广东', '上海', '山东', '浙江', '山西', '湖南', '湖北', '江西', '江苏', '贵州', '北京',
       '辽宁', '河北', '西藏', '安徽', '福建', '吉林', '海南', '重庆', '河南', '陕西', '宁夏',
       '内蒙古', '青海', '澳门', '四川', '香港', '甘肃', '云南', '新疆', '广西', '黑龙江', '天津',
       '台湾'], dtype=object)

hash_list = np.array(['天猫双11', '吴亦凡1106生日快乐', '微博橱窗', '6000多首歌从KTV下架', '6000多首歌将从KTV下架',
       '投资达人说', '原创首发', '首届中国国际进口博览会', '搞笑', '电影', '珠海航展', '2018珠海航展',
       '搞笑趣事', '搞笑幽默', '冬日城事', 'NBA吐槽大会', 'NBA', '情感', '微博公开课', '旅行灵感季',
       '双世宠妃2', '爱上券购', '搞笑视频', 'NBA零距离', '运动教室', '美食', '旅行新势力', '美食温暖你',
       '全民带货', '进博会，江苏风', '江苏自媒体联盟', '一起家庭教育', '英雄联盟S8', '贵阳身边事',
       '微博搞笑排行榜', '红人的诞生', '爱情日志', '全国消防宣传月', '点赞活力内蒙古', '动漫中心', '三分钟看电影',
       '种草预告', '开团中', '时尚V赏', '点赞或评价抽红包', '搞笑大裤衩', '美妆手帐', '美妆情报局',
       '正能量随笔', '远离负能量'], dtype=object)

#下面是想矩阵补全看看效果
data_tensor = np.load('build_tensor.npy')
data_matrix = data_tensor.sum(1)




#原始数据热力图
from pyecharts import HeatMap

dataa = [[i, j, data_matrix[i,j]] for i in range(34) for j in range(50)]
x_axis = geo_list
y_axis = hash_list
data = data_matrix
heatmap = HeatMap(width = 2000,height = 750)
heatmap.add(
    "话题热力图(观测值)",
    x_axis,
    y_axis,
    dataa,
    is_visualmap=True,
    visual_text_color="#000",
    visual_orient="horizontal",
)
heatmap.render(path = '话题热力图(观测值).html')

# 矩阵补全
X_incomplete = data_matrix
missing_mask = (X_incomplete==0)
X_incomplete[missing_mask] = np.nan
X_filled_knn = KNN(k=6).fit_transform(X_incomplete)
X_filled_nnm = NuclearNormMinimization(min_value=0).fit_transform(X_incomplete)

#knn预测数据热力图
from pyecharts import HeatMap

dataa = [[i, j, X_filled_knn[i,j]] for i in range(34) for j in range(50)]
x_axis = geo_list
y_axis = hash_list
data = data_matrix
heatmap = HeatMap(width = 2000,height = 750)
heatmap.add(
    "话题热力图(观测值)",
    x_axis,
    y_axis,
    dataa,
    is_visualmap=True,
    visual_text_color="#000",
    visual_orient="horizontal",
)
heatmap.render(path = '话题热力图(knn预测).html')

#nuclearnorm预测数据热力图
from pyecharts import HeatMap
dataa = [[i, j, X_filled_nnm[i,j]] for i in range(34) for j in range(50)]
x_axis = geo_list
y_axis = hash_list
data = data_matrix
heatmap = HeatMap(width = 2000,height = 750)
heatmap.add(
    "话题热力图(观测值)",
    x_axis,
    y_axis,
    dataa,
    is_visualmap=True,
    visual_text_color="#000",
    visual_orient="horizontal",
)
heatmap.render(path = '话题热力图(nnm预测).html')
#
