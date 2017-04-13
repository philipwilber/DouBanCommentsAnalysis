import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, Table, select


def save_to_csv(dict):
    df = pd.DataFrame(dict)
    df.to_csv('RenMinDeMingYi_Data.csv', index=False)


def save_to_excel(dict):
    df = pd.DataFrame(dict)
    df.to_excel('RenMinDeMingYi_Data.xls', index=False)


def save_to_txt(dict):
    df = pd.DataFrame(dict)
    df.to_csv('RenMinDeMingYi_Data.txt', index=False)
