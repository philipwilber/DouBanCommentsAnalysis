import sys

import constants as cons
from crawler import Crawler

if __name__ == '__main__':
    # print(s.get_all_cat_url_from_db())

    sys.setrecursionlimit(15000)  # set the maximum depth as 15000
    cr = Crawler()
    cr.main_duanping()
