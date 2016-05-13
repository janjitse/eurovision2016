from bs4 import BeautifulSoup
import re

fh = open(test_file,"r")
test_html = fh.read()
test_soup = BeautifulSoup(test_html)
tags = test_soup.findAll("a",{"class": "youtube-watch"})

def print_video_ids(input_file):
    html = open(input_file,"r")
    tags = BeautifulSoup(html.read()).findAll("a",{"class": "youtube-watch"})
    video_ids = re.findall('watch\?v=(.*?)"',str(tags))
    for l in video_ids:
        print l
