# Project: twitter_project
# Author: absin
# Date: 2021-04-22
# DESC: file for crawl musical info site


import requests
from bs4 import BeautifulSoup
import os
import util
import dload
import datetime
import imageTweetTest
from key import musical


TARGET_URL_MUSICAL = "http://ticket.interpark.com/contents/Ranking/RankList?pKind=01011&pCate=&pType=M&pDate="

# 원래 연극도 하려고 했는데 고민중..
TARGET_URL_ACTING = "http://ticket.interpark.com/contents/Ranking/RankList?pKind=01009&pCate=&pType=D&pDate="

DIR_NAME = 'musical'


keys = {
    imageTweetTest._API_KEY: musical.API_KEY,
    imageTweetTest._API_KEY_SECRET: musical.API_KEY_SECRET,
    imageTweetTest._ACCESS_TOKEN: musical.ACCESS_TOKEN,
    imageTweetTest._ACCESS_TOKEN_SECRET: musical.ACCESS_TOKEN_SECRET
}

def crawl():

    today = util._get_date(datetime.datetime.now())
    IMG_DIR = util._get_img_dir(__file__, DIR_NAME)
    TARGET_DIR = f'{IMG_DIR}/{today}'

    isGenerate = util._create_folder(TARGET_DIR)

    if isGenerate is False:
        return

    target_url = [TARGET_URL_MUSICAL]

    selector = '.rankBody'
    container = []
    img_counter = 0

    for t_url in target_url:
        # crawl from web
        _req = requests.get(t_url)
        _req.encoding = None
        html = _req.content
        _soup = BeautifulSoup(html, 'html.parser')

        infos = _soup.select(selector)

        for info in infos:
            # parsing
            title = info.select_one('.prdInfo')['title']

            _place = info.select_one('.prdInfo > a').contents[2]
            _place2 = _place.replace('\r\n\t', '')
            place = _place2.strip()

            _date = info.select_one('.prdDuration').text
            date = _date.strip()

            container.append(f'TITLE: {title}\n\nTHEATER: {place}\nDATE: {date}')

            img = info.select_one('.prds > a > img')['src']
            dload.save(img, f'{TARGET_DIR}/{img_counter}.png')

            img_counter = img_counter + 1

    imageTweetTest.post_tweet_list(container, TARGET_DIR, keys)


crawl()
