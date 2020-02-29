#coding=utf-8
import pandas as pd
import util_jichen

file_dir  = '/home/jcyang/test/20181111'
file_list = util_jichen.get_dir_list(file_dir)

data_frame = util_jichen.bulid_dataframe(file_list)

a = pd.DataFrame(data_frame)
a.to_csv('result1212.csv',index = False)
