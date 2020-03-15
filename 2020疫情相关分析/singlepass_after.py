'''
@File    : singlepass_after.py

@Modify Time        @Author         @Version    @Desciption
------------        ------------    --------    -----------
2020-03-15 16:39    Jichen Yeung    1.0         None
'''
dic = {}
f = open('SCresult.txt',mode='r')
for line in f:
    x,y = line.split(":", 1)
    dic[x] = y
f.close()

#下面是为了画图-1
lenlist = [len(i.split(', ')) for i in dic.values()]
namelist = ['武汉汽车长草','伊朗新冠肺炎','出门忘带口罩','意大利疫情','方舱医院主题曲','希腊取消火炬传递','武汉加油','境外新冠肺炎','意大利女孩作画感谢中国','我的发型复工了']
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

lenlist.reverse()
namelist.reverse()
"""
绘制水平条形图方法barh
参数一：y轴
参数二：x轴
"""
plt.barh(range(10), lenlist, height=0.7, color='steelblue', alpha=0.8)      # 从下往上画
plt.yticks(range(10), namelist)
plt.xlim(0,800)
plt.xlabel("发布量")
plt.title("2020年3月14日14-20时 Top10话题微博数量")
for x, y in enumerate(lenlist):
    plt.text(y + 0.2, x - 0.1, '%s' % y)

plt.savefig('res1.png',dpi=300,bbox_inches = 'tight')
plt.show()

#下面是为了画图-2
neglist =[round(float(i),2)  for i in list(dic.keys())]
namelist = ['武汉汽车长草','伊朗新冠肺炎','出门忘带口罩','意大利疫情','方舱医院主题曲','希腊取消火炬传递','武汉加油','境外新冠肺炎','意大利女孩作画感谢中国','我的发型复工了']
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

neglist.reverse()
namelist.reverse()
"""
绘制水平条形图方法barh
参数一：y轴
参数二：x轴
"""
plt.barh(range(10), neglist, height=0.7, color='steelblue', alpha=0.8)      # 从下往上画
plt.yticks(range(10), namelist)
plt.xlim(0,1)
plt.xlabel("发布量")
plt.title("2020年3月14日14-20时 Top10话题预警指数")
for x, y in enumerate(neglist):
    plt.text(y+0.02 , x, '%s' % y)

plt.savefig('res2.png',dpi=300,bbox_inches = 'tight')
plt.show()