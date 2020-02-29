## 一、项目说明

趋势预测小组Tensor Completion部分通过对微博信息进行汇总，基于已观测的话题热度来预测话题在未观测“地区-时间”的热度。通常指的热度包含某一话题微博的出现量，评论数量或者是点赞转发量等等。最终基于预测结果进行和可视化的呈现。

***由于数据保密协议，仅将个人参与这部分项目实现逻辑进行记录。数据、项目细节及分析结果均不会出现。随项目进行会时不时更新***

 

## 二、代码环境

项目发开主要基于python3.6，所额外需要的packages如下所示，

1. fancyimpute （python3.6）

2. pyecharts（python3.6）

3. pyten（python2.7）

Tensor completion部分使用Python2.7，因为tensor completion代码基于Pyten。Pyten已经随code附上，请运行时移动至当前路径下

 

## 三、 数据介绍 

1. 微博内容数据所有post文件

2. 趋势数据管理>微博话题>话题数据管理里面采集到的数据

Tensor Completion部分完全基于第一部分数据，所提取信息在下面代码说明预处理部分有详细介绍。第二部分数据在本小组LSTM实现过程中被使用。

 

## 四、项目流程

Tensor Completion主要分为三大模块，即对原始数据集进行预处理及简单分析、二维Completion、三维Tensor completion。其中三维Tensor completion复现了AirCP algorithm (Hancheng Ge, 2016)，流程细节如下

 

util.py：

包含了三个函数，在之后的code中会用到

1. get_dir_list #获取指定文件夹下的'post'文件

2. bulid_dataframe #输入file_list ，对所有文件进行处理，生成一个字典

3. build_tensor #输入是一个pandas dataframe，里面有地点时间hashtag，输出是3维的统计矩阵(tensor)

 

#### 数据预处理第一步：

使用函数：read_data_weibo_post.py

作用：对指定路径下所有post文件进行整理，从json条目中提取所需数据

输入：需要指定文件夹路径，如'/xx/yy/zz/20181111'

输出：result.csv文件，包含信息如下：时间、地点、hashtag、点赞数、转发数、评论数

细节：1.对没有地理信息的数据进行了过滤 2.将时间数据转化为unix时间戳 3.因为地理信息精度不同，统一处理在了省这一精度。

 

#### 数据预处理第二步：

使用函数：data description.py

所需额外package：pyecharts

作用：1. 进一步数据预处理 2. 各类可视化 3. 构建tensor并保存

输入：之前整理好的result.csv的路径

输出：1. Top50话题词云. 2. hashtag数量衰减图 3. 全国微博使用量的热力图 4. 某一话题的热力图。5. 将预处理的数据存储成三维tensor，保存在build_tensor.npy中

细节：1. 删除地理位置是“其他”与“海外”的条目，只对中国境内省市进行统计 2. 按照hashtag出现数目定义这一话题热度，选出top50的话题 3. 将时间划分区间，暂定每小时为1个区间 #time '2018-11-05 14:00:03' -> '2018-11-06 14:16:40' 4. 调用util里面的函数生成张量，并储存为build_tensor.npy。

因为tensor completion代码基于python 2.7的一些packages，所以这里需要将build_tensor.npy存储下来，然后使用另外的code进行处理

 

#### Tensor completion（1）

使用函数：matrix_com.py

所需额外package：fancyimpute pyecharts

作用：不考虑tensor时间维度，仅从地理信息和hashtag两个维度尝试对缺失值进行预测，所使用方法为KNN, NuclearNormMinimization。

输入：build_tensor.npy

输出：两种方法补全后的矩阵，并用热力图将补全前后的效果展示出来。

细节：NuclearNormMinimization方法效果更好

 

#### Tensor completion（2）

使用函数：tensor_completion.py

所需额外package：pyten

注意：由于pyten只支持python2.7，所以这部分需要python2.7运行。

作用：使用AirCP algorithm(Hancheng Ge, 2016) 进行tensor completion

输入：build_tensor.npy

输出：使用AirCP方法补全后的张量。并抽取了北京-天猫双十一 这一话题的预测效果和上海-首届中国国际进口博览会 这一话题的预测效果进行可视化。

 

 

另外，针对最新一批采集到数据有如下预处理代码

使用函数：json_to_csv.py

作用：将txt文件中的json条目中的信息提取，存为csv文件

输入：原始数据位置路径

输出：整理好的csv

 

## 五、项目评估

目前提供的模型中，可以分别从二维和三维进行tensor completion。能够对话题未观测的“地区-时间”信息进行预测。