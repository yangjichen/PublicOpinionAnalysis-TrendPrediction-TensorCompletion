'''
@File    : util.py

@Modify Time        @Author         @Version    @Desciption
------------        ------------    --------    -----------
2020-03-04 17:25    Jichen Yeung    1.0         None
'''
import os
import json
import time
import pandas as pd
import numpy as np

#获取指定文件夹下的'post'文件
def get_dir_list(file_dir):
    file_list = []
    for i in os.listdir(file_dir):
        file_list.append(file_dir + '/'+i)
    return(file_list)


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
