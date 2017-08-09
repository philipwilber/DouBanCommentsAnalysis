import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, Table, select

from pymongo import *


class DBProvider(object):
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.db = conn.DB_DOUBAN
        self.TB_ZHANLANG2 = self.db.TB_ZHANLANG2

    def add_zhanlang2(self, dict):
        self.TB_ZHANLANG2.insert(dict)

    def get_zhanlang2(self):
        return self.self.TB_ZHANLANG2.find()

    def check_record_exist(self, id):
        count = self.TB_ZHANLANG2.find({'id': id}).count()
        if count > 0:
            return True
        else:
            return False

    def save_to_csv(dict, name):
        df = pd.DataFrame(dict)
        df.to_csv(str(name) + '.csv', index=False, encoding="utf-8")

    def save_to_excel(dict, name):
        df = pd.DataFrame(dict)
        df.to_excel(str(name) + '.xls', index=False, encoding="utf-8")

    def save_to_txt(dict, name):
        df = pd.DataFrame(dict)
        df.to_csv(str(name) + '.txt', index=False, encoding="utf-8")


if __name__ == '__main__':
    s = DBProvider()
    dic = s.add_zhanlang2()
    count = 0
    print(count)
