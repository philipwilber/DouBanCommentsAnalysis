import requests
import re
from bs4 import BeautifulSoup as bs
from lxml import etree
import constants as cons
import db


def login(url):
    user_name = input('Username(Email):')
    pwd = input('Password:')

    formdata = {
        'source': 'index_nav',
        'redir': url,
        'form_email': user_name,
        'form_password': pwd,
        'login': u'登录'
    }

    s = requests.Session()
    r = s.post(cons.url_login, data=formdata, headers=cons.headers)
    content = r.text

    soup = bs(content, 'lxml')
    captcha = soup.find('img', id='captcha_image')

    if captcha:
        captcha_url = captcha['src']
        re_captcha_id = r'captcha\?id=(.*?)&'
        captcha_id = re.findall(re_captcha_id, captcha_url)
        print(captcha_id)
        print(captcha_url)
        captcha_text = input('please input the captcha:')
        formdata['captcha-solution'] = captcha_text
        formdata['captcha-id'] = captcha_id
        r = s.post(cons.url_login, data=formdata, headers=cons.headers)
    else:
        r = s.post(cons.url_login, data=formdata, headers=cons.headers)

    if r.status_code == 200:
        print('Login Success !')
        get_short_comments(r.text)
    else:
        # if page.status_code == 403:
        #     # webbrowser.open_new(url)
        #     #input_text = input("Please Enter Verification Code in Browser!")
        #     if get_auth_code() == True:
        #         pass
        #     else:
        #         return
        # else:
        # print(str(url) + ' Connection Error : ' + str(page.status_code) + ' Change to new proxy : ')
        # proxies_set = proxy.getproxy()
        # print(proxies_set)
        # return get_html(url, proxies_set, is_check_url)
        print('Login Fail !')


def get_page_txt(url):
    if ('accounts' in url):
        login(url)
    else:
        s = requests.Session()
        r = s.get(url, headers=cons.headers)
        get_short_comments(r.text)


# def get_comments(self, page_txt):
#
#     dic = {}
#     tree = etree.HTML(page_txt)
#     cmts_id_list = tree.xpath('//*[@id="comments"]/div[@class="comment-item"]/@data-cid')
#     # Add comment id
#     if len(cmts_id_list):
#         for i in range(len(cmts_id_list)):
#             id = cmts_id_list[i]
#
#
#
#             print(str())

def get_short_comments(page_txt):
    # id, user_id, user_name, status, rating, time, votes, desc, cre_date

    dict_list = []

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
            rating = str(rating_list[i])
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

            dict_list.append(dic)

            print(id)

        db.save_to_csv(dict_list)
        next_url = tree.xpath('//div[@id="paginator"]/a/@href')
        if next_url != None:
            get_page_txt(cons.url_cmts_2[0] + next_url[0])
        else:
            print('Download Complete !')


if __name__ == '__main__':
    # print(s.get_all_cat_url_from_db())
    url = cons.url + cons.url_cmts_2[0] + cons.url_cmts_2[1]
    login(url)
