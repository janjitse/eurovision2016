import pandas as pd
import numpy as np
from datetime import datetime
import sys
#Crawler from https://github.com/yuhonglin/YTCrawl
sys.path.append('D:\Python\crawler')
from crawler import Crawler

input_file = "Eurovision before 2016.csv"
test_file = "eurovision 2016.csv"
test_file2 = "eurovision 2016-2.csv"

data = pd.read_csv(input_file)
test_data = pd.read_csv(test_file)

ytcrawler = Crawler()
ytcrawler._crawl_delay_time = 1

def int_list(input_list):
    output_list = map(int,input_list)
    return output_list

def convert_to_date(input_list):
    date = datetime(year=input_list[0],month=input_list[1],day=input_list[2])
    return date

data['Contest Date'] = 0
data['Contest Date'] = data[data['Date of contest']!=0]['Date of contest'].apply(str.split,args='.').apply(int_list).apply(convert_to_date)
test_data['Contest Date'] = 0
test_data['Contest Date'] = test_data[test_data['Date of contest']!=0]['Date of contest'].apply(str.split,args='.').apply(int_list).apply(convert_to_date)

data['Videocounts'] = 0
data['Video uploaded'] = 0

test_data['Videocounts'] = 0
test_data['Video uploaded'] = 0

ytcrawler._crawl_delay_time = 1
ytcrawler.set_num_thread = 1
for l in range(data['Videocounts'].size):
    if(data.loc[l,'Videocounts']==0 and data.loc[l,'Official video']!=0):
        try:
            yt_data = ytcrawler.single_crawl(data.loc[l,'Official video'])
        except Exception as e:
            if(str(e) == 'private video'):
                continue
            if(str(e) == 'statistics disabled'):
                continue
            else:
                print e
                break
        days = (data.loc[l,'Contest Date'].to_pydatetime().date() - yt_data['uploadDate']).days
        data.loc[l,'Videocounts'] = sum(yt_data['dailyViewcount'][:days+1])
        data.loc[l,'Video uploaded'] = yt_data['uploadDate']

for l in range(test_data['Videocounts'].size):
    cur_video = test_data.loc[l,'Official video']
    if(test_data.loc[l,'Videocounts']==0 and cur_video!=0):
        try:
            yt_data = ytcrawler.single_crawl(cur_video)
        except Exception as e:
            if(str(e) == 'private video'):
                continue
            if(str(e) == 'statistics disabled'):
                continue
            else:
                print e
                break
        days = (test_data.loc[l,'Contest Date'].to_pydatetime().date() - yt_data['uploadDate']).days
        test_data.loc[l,'Videocounts'] = sum(yt_data['dailyViewcount'][:days+1])
        test_data.loc[l,'Video uploaded'] = yt_data['uploadDate']
