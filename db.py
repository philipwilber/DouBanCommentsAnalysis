import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, Table, select

class DB(object):

    def save_to_csv(self, dict):
        df = pd.DataFrame(dict)
        df.to_csv('RenMinDeMingYi_Data.csv', index=False)

    def save_to_excel(self, dict):
        df = pd.DataFrame(dict)
        df.to_excel('RenMinDeMingYi_Data.xls', index=False)

    def save_to_txt(self, dict):
        df = pd.DataFrame(dict)
        df.to_csv('RenMinDeMingYi_Data.txt', index=False)


