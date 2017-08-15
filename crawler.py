import random
import time

import sys
import requests
import re
from bs4 import BeautifulSoup as bs
from lxml import etree
import constants as cons
import proxy_collect
from db import DBProvider



class Crawler(object):
    def __init__(self):
        self.pd = DBProvider()
        self.page_index = 0
        self.record_index = 0

    def login(self, url):
        # user_name = input('Username(Email):')
        # pwd = input('Password:')
        print('Start Login')
        formdata = {
            'redir': url,
            'form_email': '',
            'form_password': '',
            'login': u'登录',
            "source": "index_nav"
        }

        s = requests.Session()
        r = s.post(cons.url_login, data=formdata, headers=cons.headers)

        content = r.text

        soup = bs(content, 'lxml')
        captcha = soup.find('img', id='captcha_image')
        if (captcha):
            r = self.get_captcha(cons.url_login, s, captcha, formdata)

        if r.status_code == 200:
            # 登录成功
            print('Login Success !')
            return self.get_short_comments(r.text, s, r.cookies)
        else:
            # 登录不成功，重新登录
            print('Login Fail !')
            time.sleep(10)
            return self.login(url)

    def get_au(self, url):
        print('Start authorize')
        formdata = {
            'ck': 'Mxfv'
        }
        s = requests.Session()
        r = s.post(url, data=formdata, headers=cons.headers)

        content = r.text

        soup = bs(content, 'lxml')
        captcha = soup.find('img', alt='captcha')
        if (captcha):
            orign_url = soup.find('input', name='original-url').get('value')
            formdata['original-url'] = str(orign_url)
            print('Authorization: ')
            r = self.get_captcha(url, s, captcha, formdata)

        if r.status_code == 200:
            print('Authorization Success !')
            time.sleep(10)
            return self.get_short_comments(r.text, s, r.cookies)
        else:
            print('Authorization Fail !')
            time.sleep(10)
            return self.login(url)

    def get_captcha(self, url, s, captcha, formdata):
        captcha_url = captcha['src']
        re_captcha_id = r'captcha\?id=(.*?)&'
        captcha_id = re.findall(re_captcha_id, captcha_url)
        print(captcha_id)
        print(captcha_url)
        captcha_text = input('please input the captcha:')
        formdata['captcha-solution'] = captcha_text
        formdata['captcha-id'] = captcha_id
        r = s.post(url, data=formdata, headers=cons.headers)
        return r

    def get_page(self, url, s, cookies, is_login):
        li = []
        if (is_login):
            time.sleep(random.uniform(0, 2))
            return self.login(url)
        else:
            time.sleep(random.uniform(0, 4))
            r = s.get(url, headers=cons.headers, cookies=cookies, timeout=cons.TIMEOUT)
            if(r.status_code == 200):
                print('url: ' + url)
                return self.get_short_comments(r.text, s, cookies)
            else:
                time.sleep(random.uniform(0, 2))
                return self.get_au(url)


    def get_short_comments(self, page_txt, s, cookies):
        # id, user_id, user_name, status, rating, time, votes, desc, cre_date
        # try:
        tree = etree.HTML(page_txt)
        cmts_id_list = tree.xpath('//div[@class="comment-item"]/@data-cid')
        user_id_list = tree.xpath('//div[@class="avatar"]/a/@href')
        user_name_list = tree.xpath('//div[@class="avatar"]/a/@title')
        status_list = tree.xpath('//span[@class="comment-info"]/span[1]/text()')
        rating_list = tree.xpath('//span[@class="comment-info"]/span[2]/@class')
        time_list = tree.xpath('//span[@class="comment-time "]/@title')
        votes_list = tree.xpath('//span[@class="votes"]/text()')
        desc_list = tree.xpath('//div[@class="comment"]/p')
        index = len(cmts_id_list)
        if index != len(user_id_list) \
                or index != len(user_name_list) \
                or index != len(status_list) \
                or index != len(rating_list) \
                or index != len(time_list) \
                or index != len(votes_list) \
                or index != len(desc_list):
            print('xpath error !')
        else:
            re_user_id = r'people\/(.*?)\/'
            for i in range(len(cmts_id_list)):
                id = int(cmts_id_list[i])
                user_id = re.findall(re_user_id, user_id_list[i])[0]
                user_name = str(user_name_list[i])
                status = status_list[i]
                rating = self.get_re_digits(str(rating_list[i]))
                time = str(time_list[i])
                votes = votes_list[i]
                desc = str(desc_list[i].xpath('string(.)')).strip()
                dic = {'id': id,
                       'user_id': user_id,
                       'user_name': user_name,
                       'status': status,
                       'rating': rating,
                       'time': time,
                       'votes': votes,
                       'desc': desc}
                if (not self.pd.check_record_exist_zhanlang2(id)):
                    self.pd.add_zhanlang2(dic)
                    print(id)
                    self.record_index += 1
            self.page_index += 1
            print('Number of records : ' + str(self.record_index))
            print('Number of pages : ' + str(self.page_index))
            next_url = tree.xpath('//div[@id="paginator"]/a[@class="next"]/@href')
            if next_url != None:
                return [cons.url_zhanlang2 + cons.url_cmts_2[0] + next_url[0], s, cookies]
            else:
                return ['', s, cookies]

    def get_re_digits(self, target_str):
        search_data = re.compile(r'\d+\.?\d*')
        li = search_data.findall(target_str)
        value = ''
        if len(li) > 0:
            value = li[0]
        return value

    '''
     最初版本使用函数递归作为规则获取数据，但因为python的递归深度限制会造成栈溢出
     因此添加main方法，使用循环控制爬虫流程，尽量减少使用递归
    '''
    def main_duanping(self):
        is_login = True
        url = ''
        s = None
        cookies = None
        # 获取短评
        url = cons.url_zhanlang2 + cons.url_cmts_2[0] + cons.url_cmts_2[1]
        while len(url) > 0:
            li = self.get_page(url, s, cookies, is_login)
            url = li[0]
            s = li[1]
            cookies = li[2]
            is_login = False
        print('Load Completed !')
