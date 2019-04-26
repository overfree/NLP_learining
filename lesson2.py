#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author：dacong time:2019/4/16
import os
import pandas as pd
database = 'D:\\dacong_work\\NLP\\export_sql_1558435\\sqlResult_1558435.csv'
os.path.exists(database)
dataframe = pd.read_csv(database,encoding='gb18030')
print(dataframe)
