import pandas as pd
from pandas import json_normalize
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false')
filter={}
result = client['gyan']['course'].find(
  filter=filter 
)
db = client['gyan']
