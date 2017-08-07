import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, Table, select


def save_to_csv(dict, name):
    df = pd.DataFrame(dict)
    df.to_csv(str(name) + '.csv', index=False, encoding="utf-8")


def save_to_excel(dict, name):
    df = pd.DataFrame(dict)
    df.to_excel(str(name) + '.xls', index=False, encoding="utf-8")


def save_to_txt(dict, name):
    df = pd.DataFrame(dict)
    df.to_csv(str(name) + '.txt', index=False, encoding="utf-8")
