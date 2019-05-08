# -*- coding: utf-8 -*-
import scrapy
import xlwt
import xlrd
from xlutils.copy import copy
import re
from copy import deepcopy
from bs4 import BeautifulSoup


class GsSpider(scrapy.Spider):
    name = 'gs'
    allowed_domains = ['scjgj.sh.gov.cn']
    start_urls = ['http://scjgj.sh.gov.cn/shaic/faq!getList.action']
    baseUrl = 'http://scjgj.sh.gov.cn/shaic/'

    def parse(self, response):
        # 来记录爬取的地址
        hrefs = {}

        # 来记录内容

        html_doc = response.body
        # html_doc = html_doc.decode('utf-8')
        soup = BeautifulSoup(html_doc, 'html.parser')
        # 得到table里面的值
        contxt = soup.select('.div_questions_list')

        # print(contxt)
        # 遍历里面的tr标签
        for temp in range(0,len(contxt[0].select('li'))):
            item = {}

            li = contxt[0].select('li')[temp]

            # 得到a标签里面的值
            href = li.select('a')[0]
            # print(href)
            href = li.select('a')[0].attrs['href']
            hrefs["href"]=self.baseUrl+href

            temp+=1

            yield scrapy.Request(
                hrefs["href"],
                callback=self.parse_answer,
                meta = {"hrefs":deepcopy(hrefs),"item":deepcopy(item)}
            )

        # 翻页
        # 正则获得页码
        page_count = int(re.findall(">共.*?页</td>",response.body.decode))
        current_page = int(re.findall(">当前第.*?页</td>",response.body.decode))
        if current_page<page_count:
            next_url = self.start_urls[0]+"?p="+str(current_page+1)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    # 详情页面
    def parse_answer(self, response):
        item = response.meta["item"]
        # 来解析详情页面记录信息
        html_doc = response.body
        # res.encoding = 'utf-8'
        soup = BeautifulSoup(html_doc, 'html.parser')
        contxt = soup.select('.div_questions')
        # 解析问题和答案
        ques = contxt[0].select('.h10')[0].get_text()
        answer = contxt[0].select('.questions_content')[0].get_text()
        # # 打开excel
        # rb = xlrd.open_workbook("工商常见问题.xls")
        # r_sheet = rb.sheet_by_index(0)
        # # 得到行数
        # rows = r_sheet.nrows
        # # 复制 excel 操作
        # wb = copy(rb)
        # sheet = wb.get_sheet(0)
        # sheet.write(rows, 0, ques)
        # sheet.write(rows, 1, answer)
        # # 保存
        # wb.save("工商常见问题.xls")
        print(ques)
        print(answer)
