import os
import json
import time
import pandas as pd
import numpy as np

#获取指定文件夹下的'post'文件
def get_dir_list(file_dir):
    file_list = []
    for i in os.listdir(file_dir):
        if (i.find('post') != -1):
            file_list.append(file_dir + '/'+i)
    return(file_list)


#输入file_list ，对所有文件进行处理，生成一个字典
#提取的信息：time location hashtag commentcount likecount sharecount
def bulid_dataframe(file_list):
    data_frame = {}
    timee = []
    hashtag = []
    geo = []
    comment_count = []
    like_count = []
    share_count = []
    for filename in file_list:
        with open(filename, 'r') as f:
            for line in f:
                curr = json.loads(line)
                # print(curr)
                if (curr['topicTitles'] != None and curr['author']['location'] != None):

                    for i in range(len(curr['topicTitles'])):
                        geolocate = curr['author']['location'].split(' ')[0]
                        hash = curr['topicTitles'][i]
                        timestamp = curr['publishDate']
                        com = curr['commentCount']
                        lik = curr['likeCount']
                        sha = curr['shareCount']

                        # time_local = time.localtime(curr['publishDate'])
                        # timestamp = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                        geo.append(geolocate)
                        timee.append(timestamp)
                        hashtag.append(hash)
                        comment_count.append(com)
                        like_count.append(lik)
                        share_count.append(sha)

        data_frame['time'] = timee
        data_frame['location'] = geo
        data_frame['hashtag'] = hashtag
        data_frame['commentcount'] = comment_count
        data_frame['likecount'] = like_count
        data_frame['sharecount'] = share_count
    return (data_frame)


#输入是一个pandas dataframe，里面有地点时间hashtag，输出是3维的统计矩阵(tensor)
def build_tensor(data):
    geo_list = pd.unique(data['location'])
    time_list = list(range(24))
    hash_list = pd.unique(data['hashtag'])

    dict1 = dict(zip(geo_list,range(len(geo_list))))
    dict2 = dict(zip(time_list,range(len(time_list))))
    dict3 = dict(zip(hash_list,range(len(hash_list))))


    tensorr = np.zeros( (len(geo_list), len(time_list), len(hash_list)))
    for i in range(len(data)):
        location = data.iloc[i]['location']
        time = data.iloc[i]['fenzu']
        tag = data.iloc[i]['hashtag']
        tensorr[dict1[location], dict2[time], dict3[tag]] += 1

    return(tensorr,geo_list,hash_list)