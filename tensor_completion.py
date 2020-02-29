# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import numpy as np
import pyten



path = '/Users/yangjichen/Desktop/项目/舆情分析-tensor/code/jichentest/'
data_tensor = np.load('build_tensor.npy')

#利用pyten里面的构建的ten_class
data_tensor = pyten.tenclass.tensor.Tensor(data_tensor)
#可以看到的位置在omega中记作1
Omega = (data_tensor.data>0).astype(np.int8)
alp = 0.1*np.ones(3)
lam = 1e-3

self = pyten.method.AirCP(data_tensor, omega = Omega,rank=4,max_iter=3000,lmbda=lam, alpha = alp)
self.run()
rX1 = self.X

#res就是最终补全后的张量
res = self.X.data
neg = float(np.sum(res<0))/float(np.prod(data_tensor.shape))
print(neg)
print(res)

# #比较matlab的热力图
from pyecharts import HeatMap
data_matrix = res[:,:,1]

dataa = [[i,j, data_matrix[i,j]] for i in range(34) for j in range(24)]
heatmap = HeatMap(width = 2000,height = 750)
heatmap.add(
    "话题热力图(观测值)",
    range(34),
    range(24),
    dataa,
    is_visualmap=True,
    visual_text_color="#000",
    visual_orient="horizontal",
)
heatmap.render(path = '热力图.html')


#关于北京 天猫双十一这一话题的预测效果

from pyecharts import Line
line = Line('北京-天猫双十一')
x = rX1.data[10,:,0]
y = data_tensor.data[10,:,0]
line.add('prediction',list(range(24)),x,is_smooth=True,
    is_fill=True,
    line_opacity=0.2,
    area_opacity=0.4,
    symbol=None,)
line.add('observed',list(range(24)),y)
line.render(path = '北京-天猫双十一.html')

#关于上海 首届中国国际进口博览会 这一话题的预测效果
from pyecharts import Line
line = Line('上海-首届中国国际进口博览会')
x = rX1.data[1,:,7]
y = data_tensor.data[1,:,7]
line.add('prediction',list(range(24)),x,is_smooth=True,
    is_fill=True,
    line_opacity=0.2,
    area_opacity=0.4,
    symbol=None,)
line.add('observed',list(range(24)),y)
line.render(path = '上海-首届中国国际进口博览会.html')