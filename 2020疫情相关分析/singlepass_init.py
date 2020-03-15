'''
@File    : singlepass_init.py

@Modify Time        @Author         @Version    @Desciption
------------        ------------    --------    -----------
2020-03-15 12:32    Jichen Yeung    1.0         None
'''
import requests
from urllib.parse import urlencode
import pandas as pd


def get_data(scroll='', b_t='', e_t='',title=''):
    """
    通过定位符获取数据
    :param e_t: str, 截止时间
    :param b_t: str, 开始时间
    :param scroll: str, 定位符
    :return:
            scroll: str, 定位符
            data_list: list, 数据
    """
    base_url = 'Server地址'
    params = {
        'appkey': '5dkg44',
        'scrollId': scroll,
        'title': title,
        'crawl_time_min': b_t,
        'crawl_time_max': e_t
    }
    url = base_url + urlencode(params)
    response = requests.get(url, timeout=10)
    j = response.json()

    scrollID = j.get('scrollId')
    total = j.get('total')
    data_list = j.get('data')
    print('Total num = '+str(total) + ', obtain num = '+ str(len(data_list)))

    #return j ,data_list
    return scrollID, data_list



if __name__ == '__main__':
    name = '20200314'
    b_t = '2020-03-14 14:00:00'
    e_t = '2020-03-14 20:00:00'

    title = ''
    full_data = []
    scrollid = ''

    while True:
        try:
            scrollid, data_list = get_data(scroll = scrollid,b_t=b_t,e_t=e_t,title=title)
            full_data = full_data+data_list
        except:
            break

    full_data = pd.DataFrame(full_data)
    full_data = full_data[['id','created_at','attitudes_count','comments_count','reposts_count','raw_text','user']]
    full_data.to_csv('./疫情数据/' + name + '.csv', sep=',')
