from bs4 import BeautifulSoup
from urllib.request import urlopen
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import platform
import numpy as np
from PIL import Image
import csv
import collections
collections.Callable = collections.abc.Callable

html = urlopen('https://www.youthdaily.co.kr/news/article.html?no=145528')
bs = BeautifulSoup(html, 'html.parser')
article = bs.find('div', {'id':'news_bodyArea'}).find_all('p')
#print(article)

aList = []
for a in article :
    try :
        print(a.text)
        aList.append(a.text)
    except a.text=='':
        pass

def make_wordcloud(title_list, stopwords, word_count):
    okt = Okt()
    sentences_tag = []
    for sentence in title_list:
        morph = okt.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-'*80)

    noun_adj_list=[]

    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun']:
                noun_adj_list.append(word)
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    print('-'*80)
    print(tags)

    tag_dict = dict(tags)

    for stopword in stopwords:
        if stopword in tag_dict:
            tag_dict.pop(stopword)
    print(tag_dict)

    if platform.system() == 'Windows':
        path = r'c:\Windows\Fonts\malgun.ttf'
    else:
        font = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

    img_mask = np.array(Image.open('marketing.png'))
    wordcloud = WordCloud(font_path = path, width=800, height=600, background_color=None, mode='RGBA',
                   max_font_size=200, repeat=True, colormap='inferno', mask=img_mask)

    cloud = wordcloud.generate_from_frequencies(tag_dict)
    wordcloud.to_file('마케팅' + '.png')
    plt.figure(figsize=(10,8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()

stopwords = ['데이터', '있다', '성형', '생', '엔비디아', '를', '기술', '활용', '벌', '으', '수', '이', '다른']
make_wordcloud(aList, stopwords, 50)