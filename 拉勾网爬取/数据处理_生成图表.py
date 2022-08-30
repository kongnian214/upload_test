import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = [u'simHei']   # 设置中文
plt.rcParams['axes.unicode_minus'] = False   # 正常显示负号
pd.set_option('display.max_columns', None)   # 显示完整的列
pd.set_option('display.max_rows', None)  # 显示完整的行
pd.set_option('display.expand_frame_repr', False)  # 设置不折叠数据

all=pd.read_csv('all.csv',encoding='gbk',index_col=0)
all = pd.DataFrame(all)

# 色彩函数
def colors(input_data):

    color = cm.RdYlGn(np.linspace(0, 1, len(input_data)))
    return color
#生成图表
city_data=all['所在城市'].value_counts().sort_index().sort_values()
city_data.plot(kind='bar',color=colors(city_data))
# plt.show()
plt.savefig('need_image.jpg')
word_age=all['工作年限'].value_counts().sort_index()
word_age.plot(kind='bar',color=colors(word_age))
# plt.show()
plt.savefig('age_image.jpg')
education=all['学历状况']
education.value_counts().sort_index().plot(kind='bar',color=colors(education))
# plt.show()
plt.savefig('education_image.jpg')

#分割工资
salary = all['工资'].str.split('-', expand=True)
# print(salary)
all['最小工资']=salary[0]
all['最大工资']=salary[1]
salary = all['最小工资'].str.split('k', expand=True)
all['最小工资']=(salary[0].astype(int))*1000
# print(all['最小工资'])
salary = all['最大工资'].str.split('k', expand=True)
all['最大工资']=(salary[0].astype(int))*1000
salary_list=[]
salary_list_max=[all['最大工资']]
salary_list_min=[all['最小工资']]
for max,min in  zip(salary_list_max[0],salary_list_min[0]):
    salary_list.append((max+min)/2)
all['平均']=salary_list
#获得 最小工资','最大工资' ,'平均' 写入一个新的表
# all.to_csv(r"new_test.csv",mode = 'a',index =False,encoding='gbk')##处理工资数据写入 无法重复写入覆盖要重新创建文件
# all = all.drop_duplicates(subset = ['公司的全称','招聘岗位名称','工资'] ,keep = 'first',inplace=False)#去除重复行

##-----工资图--------
salary_data = all[['最小工资','最大工资' ,'平均']]
salary_data.index=all['所在城市']
salary_data.index.name='所在城市'
salary_data.columns=['最小工资','最大工资' ,'平均']
salary_data_indexs = all['所在城市'].drop_duplicates().tolist()

data_list = []
for i in salary_data_indexs:
    # print(i)
    loc_data = salary_data.loc[i, :]
    if type(loc_data) == pd.Series:
        data_list.append(loc_data)
    else:
        salary_all_mean = loc_data.mean(axis=0).round(2)
        data_end = pd.Series(salary_all_mean).rename(i)
        data_list.append(data_end.to_frame())
# print(data_list)
salary_data_end = pd.concat((data_list), axis=1).T
# print(salary_data_end)
salary_data_end['城市'] = salary_data_end.index
# print(salary_data_end)
salary_data_end.plot(x='城市', y=['最小工资','平均' ,'最大工资'], kind="bar", figsize=(15, 8))
plt.tight_layout()
# plt.show()
# plt.savefig('salary.jpg')


#-------词云-----
#写入txt 词云
import jieba
with open('Alice.txt', 'w', encoding='utf-8') as ff:
    for G in all['岗位描述']:
        text =G.replace('\\', '').replace('[', '').replace(']', '').replace("'", '').replace(',', '').replace(' ', '').strip()
        # 1.对文本进行分词
        words = jieba.cut(text, cut_all=False)
        # 2.去除停用词
        with open('中文停用词库.txt', 'r', encoding='utf-8')as f:
            stopwords = f.read()
        words = [i for i in words if i not in stopwords]
        for i in words:
            ff.write(i+' ')
#画图
from wordcloud import WordCloud
from PIL import Image
import numpy as np
# mask = np.array(Image.open('apple.jpg'))

f = open('Alice.txt','r',encoding = 'utf-8')
txt = f.read()
f.close()
wordcloud = WordCloud(background_color="white",
                      font_path='C:\Windows\Fonts\msyh.ttc',
                      width = 800,height = 600,).generate(txt)
wordcloud.to_file('词云.jpg')