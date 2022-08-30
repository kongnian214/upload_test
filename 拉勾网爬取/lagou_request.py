from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random  # 随机模块
import csv
import re

with open('all.csv', 'w', newline='') as f:
    csv_all = csv.writer(f)
    csv_all.writerow(['公司的全称', '招聘岗位名称', '工资', '所在城市', '工作年限', '学历状况', '公司标签', '详情页url地址', '岗位描述'])
time_end=''
class lagouSpitder(object):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver_path = r'C:\Users\kong\AppData\Local\Google\Chrome\Application\chromedriver.exe'  # 定义好路径

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=lagouSpitder.driver_path,
                                       options=lagouSpitder.option)  # 初始化路径+规避检测selenium框架
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
        })
        self.url = 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
        self.positions = []

    def userlogin(self):
        url_loign='https://passport.lagou.com/login/login.html'
        self.driver.get(url_loign)
        print(time.ctime())
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.NAME, 'account').send_keys('18077718310')
        self.driver.find_element(By.XPATH, '//*[@name="password"]').send_keys('LCs18077718310!')  #
        self.driver.find_element(By.XPATH, '//*[@class="sc-furwcr bVYGWy"]').click()
        self.driver.find_element(By.XPATH, '//*[@class="sc-fFeiMQ hmmuaS"]').click()
        time.sleep(30)
        print(time.ctime())


    def run(self):  # 主页面
        time.sleep(2)

        self.driver.get(self.url)  # 去请求主页面
        while True:
            source = self.driver.page_source  # source页面来源  先获取一页
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@action="next"]'))
            )  # 等待按钮加载出来，避免没加载出来就点击导致的报错
            self.parse_list_page(source)  # 解析完获取的这一页职位之后，去点击下一页
            next_btn = self.driver.find_element_by_xpath('//span[@action="next"]')  # 下一页的元素位置
            if "pager_next pager_next_disabled" in next_btn.get_attribute('class'):  # 如果class等于最后一页则停止，否则继续点击
                break
            else:
                next_btn.click()  # 点击下一页
                time.sleep(1)

    def parse_list_page(self, source):  # 获取职位详情页url
        html = etree.HTML(source)
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:  # 循环去解析详情页
            self.request_detall_page(link)
            time.sleep(random.uniform(1, 3))  # 随机暂停

    def request_detall_page(self, url):  # 去请求细节页面
        # self.driver.get(url)
        self.driver.execute_script("window.open('%s')" % url)  # 新打开一个职位页面
        self.driver.switch_to.window(self.driver.window_handles[1])  # 切换到当前页面来解析，不切换的话selenium会停留在上一页
        source = self.driver.page_source  # source页面来源
        self.pares_detail_page(source)  # 解析页面
        self.driver.close()  # 解析完关闭页面
        time.sleep(0.5)
        self.driver.switch_to.window(self.driver.window_handles[0])  # 切换回主页面

    def pares_detail_page(self, source):  # 获取职位细节信息
        html = etree.HTML(source)
        companyFullName= html.xpath('//h3[@class="fl"]/em/text()')[0]  # 公司的全称
        positionName  = html.xpath('//*[@class="position-head-wrap-position-name"]/text()')[0]  # 招聘岗位名称
        salary= html.xpath('//*[@class="salary"]/text()')[0] # 工资
        city  = html.xpath('//*[@class="work_addr"]/a/text()')[0]  # 所在城市 #建议去掉[0]
        createTime = html.xpath('//*[@id="__next"]/div[2]/div[1]/div/div[1]/dd/h3/span[2]/text()')[1] # 工作年限
        education = html.xpath('//*[@id="__next"]/div[2]/div[1]/div/div[1]/dd/h3/span[3]/text()') # 学历状况

        financeStage = html.xpath('//*[@id="job_company"]/dd/ul/li/h4/text()')[:3]  # 公司标签
        # url=html.xpath('//a[@class="position_link"]/@href')#详情页url
        url=self.driver.current_url
        positionLables = html.xpath('//div[@class="job-detail"]//text()')# 岗位描述

        position = {
            '公司的全称': companyFullName,
            '招聘岗位名称': positionName ,
            '工资': salary ,
            '所在城市 ': city ,
            '工作年限': createTime,
            '学历状况': education,
            '公司标签':financeStage,
            '详情页url地址': url,
            '岗位描述':positionLables,

        }
        self.positions.append(position)
        print(position)
        print('=' * 40)
        with open('all.csv', 'a+', newline='') as f:
            csv_all = csv.writer(f)
            try:
                csv_all.writerow(
                    [companyFullName, positionName,salary, city, createTime,education, financeStage,url,positionLables])
            except:
                pass
        print(all)
        time.sleep(1)



if __name__ == '__main__':
    spider = lagouSpitder()
    spider.userlogin()
    spider.run()

