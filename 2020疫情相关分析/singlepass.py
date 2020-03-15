'''
@File    : singlepass.py

@Modify Time        @Author         @Version    @Desciption
------------        ------------    --------    -----------
2020-03-11 16:11    Jichen Yeung    1.0         None
'''
import numpy as np
import jieba
from gensim import corpora, models, similarities, matutils
import pandas as pd
from aip import AipNlp


def getStopWords():
    stopwords = []
    for word in open("stopwords.txt", "r"):
        stopwords.append(word.strip())
    return stopwords



#每一行都可以切割，最后返回一个list
def cutContent(content, stopwords):
    cutWords = []
    words = jieba.cut(content)
    #print words
    for word in words:
        if word == u' ':
            continue
        if word not in stopwords:
            cutWords.append(word)
            #print unicode(word)
    return cutWords

def getMaxSimilarity(dictTopic, vector):
    maxValue = 0
    maxIndex = -1
    for k,cluster in dictTopic.items():
        oneSimilarity = np.mean([matutils.cossim(vector, v) for v in cluster])
        if oneSimilarity > maxValue:
            maxValue = oneSimilarity
            maxIndex = k
    return maxIndex, maxValue


def single_pass(corpus, titles, thres):
    dictTopic = {}
    clusterTopic = {}
    numTopic = 0
    cnt = 0
    for vector, title in zip(corpus, titles):
        if numTopic == 0:
            dictTopic[numTopic] = []
            dictTopic[numTopic].append(vector)
            clusterTopic[numTopic] = []
            clusterTopic[numTopic].append(title)
            numTopic += 1

        else:
            maxIndex, maxValue = getMaxSimilarity(dictTopic, vector)

            # join the most similar topic
            if maxValue > thres:
                dictTopic[maxIndex].append(vector)
                clusterTopic[maxIndex].append(title)
            # else create the new topic
            else:
                dictTopic[numTopic] = []
                dictTopic[numTopic].append(vector)
                clusterTopic[numTopic] = []
                clusterTopic[numTopic].append(title)
                numTopic += 1
        cnt += 1
        if cnt % 1000 == 0:
            print("processing {}".format(cnt))
    return dictTopic, clusterTopic

#利用百度api做情感分析
def sentimentClassify(text):
    APP_ID = '个人信息'
    API_KEY = '个人信息'
    SECRET_KEY = '个人信息'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    result = client.sentimentClassify(text)

    return(result['items'][0]['sentiment'])






if __name__ == '__main__':
    df = pd.read_csv('./疫情数据/' + '20200314' + '.csv', sep=',', index_col=0,engine='python')
    stopWords = getStopWords()
    raw_text = df['raw_text'].astype(str)

    n = len(raw_text)
    print ('total records:', n)

    cutData = []
    for i in range(n):
        cutData.append(cutContent(raw_text[i], stopWords))
    print ('cutData is done')
    #get VSM
    dictionary = corpora.Dictionary(cutData)

    corpus = [dictionary.doc2bow(title) for title in cutData]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    thres = 0.5

    dictTopic, clusterTopic = single_pass(corpus_tfidf, list(raw_text), thres)


    #按照热点包含的话题数量排序热点
    top = list(dict(sorted(clusterTopic.items(), key=lambda d: len(d[1]),reverse = True)[:10]).values())
    res = []
    for topic in top:
        neg_idx = 0
        for text in topic:
            try:
                idx = sentimentClassify(text)
                if idx ==0: neg_idx = neg_idx+1
            except:
                continue
        res.append(neg_idx/len(topic))
    print(res)


    #保存分析结果
    import json
    dic = {}
    for i,j in zip(res,top):
        dic[i]=j

    f = open('SCresult.txt', 'w')
    for key, value in dic.items():
        f.write(str(key) + ':' + str(value))
        f.write('\n')
    f.close()








