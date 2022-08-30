
import requests
import re
import time
from bs4 import BeautifulSoup
import csv


key_word = 'python'  # 查询的关键字

#获取原码信息
def getContent(page):
    url = 'https://s.gxrc.com/sJob?district=1&pageSize=20&orderType=0&listValue=1.hml'+'.hml&keyword={}&page={}'.format(key_word, page)
    html = requests.get(url).content.decode("utf-8") # 获取网页信息
    return html

def getInfo(html):
    '''一页信息有20个'''
    ws=[]
    job_name, job_edu, job_expe, job_requirement,job_fS= [], [], [], [],[]  # 岗位名字，学历， 经验， 岗位要求都是列表形式存放
    ent_name = re.findall(r'class="entName">(.*?)</a>', html)           # 公司名字
    price = re.findall(r'<li class="w3">(.*?)</li>', html)[1:]          # 薪资
    city = re.findall(r'<li class="w4">(.*?)</li>', html)[1:]           # 工作地
    # refresh_time = re.findall(r'<li class="w5">(.*?)</li>', html)[1:]   # 更新时间
    deatil_info_url = re.findall(r'<a href="//(.*?)" target="_blank" class="posName">', html)   # 详细信息的页面网址，用于爬取职位要求和描述
    for url in deatil_info_url:
        url = "https://"+url
        html = requests.get(url).content.decode('utf-8') # 进一步解析网页的信息，获得职位名称和岗位要求两个信息
        name = re.findall(r'<h1 title="(.*?)">', html)[0] # 只有一个
        edu = re.findall(r'</span>学历(.*?)<span class="vl">', html)[0]  # 学历
        expe = re.findall(r'</span>经验(.*?)<span class="vl">', html)[0]  # 经验
        soup = BeautifulSoup(html, "html.parser")  # 正则无法完全匹配岗位要求，所以采用BeautifulSoup
        requirement = soup.find(id='examineSensitiveWordsContent').text  # 岗位要求
        fS = soup.find(id='entDetails').find_all('span')[1].text
        job_name.append(name)
        job_edu.append(edu)
        job_expe.append(expe)
        job_fS.append(fS)
        job_requirement.append(requirement)
        time.sleep(1)
    for i in range(0, 20):
        ws.append([ent_name[i],job_name[i],  price[i], city[i],
                   job_expe[i],job_edu[i], job_fS[i], deatil_info_url[i],job_requirement[i].replace('\n', '').replace('\r', '')])

    with open('data.csv', mode='a', newline='', encoding='utf-8-sig') as f:
        titles = ['companyFullName', 'positionName', 'salary', 'city', 'createTime', 'education', 'financeStage',
                  'url','positionLables']
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(titles)
        for j in ws:
            csv_writer.writerow(j)

def main():  # 页码和对应着的文件名字次数，以防读写卡死
    total_page = 15    # 最大页码数
    for page in range(1, total_page+1):
        try:
            print("正在爬取第{}页".format(page))
            html = getContent(page)  # 一页一页获取数据
            if page % 5 == 0:  # 爬到了10的倍数，暂停2s
                time.sleep(2)
            getInfo(html)  # 传入一页的页面信息和对应的表格去
        except Exception as e:
            print(e)
if __name__ == '__main__':
    main()

