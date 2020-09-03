import pandas as pd
import glob
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pandas import Series
import math
import csv
import os
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import time
import re
import random
from datetime import datetime
random.seed(datetime.now())

print('Comenzando a correr el script')

data_final = pd.read_csv("Data final limpia.csv",sep = ',')
urls_list = data_final["urls"].unique()
urls_list = [url[:url.find('?ref=')] + '/comments' for url in urls_list]

useless_characters = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')

def getPageText(url):
    #driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    driver.get(url)
    time.sleep(10)
    count = 0
    #while True:
    while (count<13):
        try:
            loadMoreButton = driver.find_element_by_xpath('//*[@id="react-project-comments"]/div/button')
            time.sleep(2)
            loadMoreButton.click()
            time.sleep(5)
            count += 1
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            break

    time.sleep(5)
    comments = driver.find_elements_by_css_selector('span.bg-ksr-green-700.white.px1.type-14.mr1, div.w100p')
    project_paragraphs = []
    for paragraph in comments:
        project_paragraphs.append(paragraph.text) 
    idx_comment_creador = [i for i in range(len(project_paragraphs)) if project_paragraphs[i] == "Creator"] 
    idx_comment_creador = [i+1 for i in idx_comment_creador]

    for index in sorted(idx_comment_creador, reverse=True):
        del project_paragraphs[index]
 
    idx_comment_creador = [i for i in range(len(project_paragraphs)) if project_paragraphs[i] == "Creator"]

    for index in sorted(idx_comment_creador, reverse=True):
        del project_paragraphs[index]

    project_paragraphs = [x for x in project_paragraphs if ("This comment") not in x]
    project_paragraphs = [x for x in project_paragraphs if ("0:00") not in x]
    project_paragraphs = [x for x in project_paragraphs if ("Showing ") not in x]
    project_paragraphs = [x for x in project_paragraphs if x]
    project_comments = []
    for project_text in project_paragraphs:
        project_text = project_text.replace(u'\xa0', u'')
        project_text = project_text.replace(u'\n', u' ')
        project_text = re.sub(useless_characters, '', project_text)
        project_comments.append(project_text)
        project_comments.append('中中中')

    del(project_paragraphs)
    project_comments = ' '.join(project_comments)    #Para concatenar todos los comentarios en 1 array
    time.sleep(randint(10,100))
    return project_comments

print("Scraping...")

ids_adic=[1119957643,
 1237497504,
 1357810203,
 148069053,
 1484371707,
 1601929183,
 1724641191,
 184740828,
 1969564786,
 2096086860,
 283473954,
 405995392,
 52687056,
 64626198,
 759831834,
 879587664]

urls_adic=['https://www.kickstarter.com/projects/hometunnel/hometunnel-vpn-reach-your-soho-network-from-everyw?ref=discovery_category_newest',
 'https://www.kickstarter.com/projects/immabee/immabe-emoji-join-the-swarm-bee-part-of-the-invasi?ref=category_newest',
 'https://www.kickstarter.com/projects/lpsmarttech/lpreader-reads-printed-text-out-loud?ref=discovery_category_newest',
 'https://www.kickstarter.com/projects/1397300529/railsapp?ref=discovery_category_newest',
 'https://www.kickstarter.com/projects/675711226/luminous-tales?ref=category_newest',
 'https://www.kickstarter.com/projects/1013189283/quicktask?ref=discovery_category_newest',
 'https://www.kickstarter.com/projects/2142529557/getcerti-app-get-certificate-from-stars-and-events?ref=category_newest',
 'https://www.kickstarter.com/projects/178023282/piso-the-most-versatile-flash-drive-yet?ref=discovery_category_newest',
 'https://www.kickstarter.com/projects/423557947/nokanye-kanye-kardashian-blocker-app?ref=category',
 'https://www.kickstarter.com/projects/bobblockus/usa-yachtsorg?ref=category_newest',
 'https://www.kickstarter.com/projects/1553792197/rushbottom-journal-redefining-traditional-relation?ref=category_newest',
 'https://www.kickstarter.com/projects/mementosmartframe/memento-smart-frame-worlds-most-advanced-4k-smart?ref=discovery_category_newest',
 'https://www.kickstarter.com/projects/1789173116/gymatch-connecting-you-with-people-that-can-help-u?ref=category_newest',
 'https://www.kickstarter.com/projects/bellalife/lifefile?ref=category',
 'https://www.kickstarter.com/projects/1866865027/nixie-bargraph-kit?ref=discovery_category_newest',
 'https://www.kickstarter.com/projects/1318970768/boxingwithstrangers?ref=discovery_category_newest']

count_proj=0
#count_proj=25548
for id_proj, url_proj in zip(ids_adic, urls_adic):
    comments_txt = getPageText(url_proj)    
    df_comments = {"ids":[id_proj], "comments":[comments_txt]}
    data_comments = pd.DataFrame(df_comments)
    data_comments.to_csv (r'data_comentarios_p16.csv', mode = 'a', sep = ',', index = False, header=False)
    count_proj += 1
    print(count_proj)

print('Ya terminó el scraping!')
driver.close()

#extension = '.csv'
#all_filenames = [i for i in glob.glob('*'.format(extension))]

#combine all files in the list
#data_comments = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
#data_comments.to_csv('data_comentarios.csv', index=False, encoding='utf-8-sig')
#df_final = pd.read_csv('data_comentarios.csv',sep = ',', header=None, names = ['comments','ids'])
#df_final = df_final.reindex(columns=['ids','comments'])
#df_final.to_csv( "data_comentarios_final.csv", index=False, encoding='utf-8-sig')
