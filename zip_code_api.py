#!/usr/bin/env python
# coding: utf-8


import pandas as pd

zip_code = pd.read_csv('uszips.csv', usecols=['zip', 'city', 'state_name'],index_col= False)
# import the module
from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="zip_code"))
data.to_sql('zip_code', con = engine, if_exists = 'append')

