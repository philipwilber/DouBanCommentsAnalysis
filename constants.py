url_login = 'https://accounts.douban.com/login'
url_zhanlang = 'https://movie.douban.com/subject/24753810'
url_zhanlang2 = 'https://movie.douban.com/subject/26363254'
# 评价
url_cmts_1 = ['collections', 'wishes', 'doings']
# 短评
url_cmts_2 = ['/comments', '?start=%s&limit=20&sort=new_score&status=P']
# url_cmts_2 = ['/comments', '?start=115000&limit=20&sort=new_score&status=P']
# 剧评
url_cmts_3 = '/reviews'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

TIMEOUT = 1000
