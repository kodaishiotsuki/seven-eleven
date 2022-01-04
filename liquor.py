import requests
import pandas as pd
import pprint
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# with urlopen("") as res:
#     html = res.read().decode("utf-8")

# 取得したデータを入れる空のリスト
d_list=[]
# ジモティーの「お酒」カテゴリーより情報を収集
url="https://jmty.jp/fukuoka/sale-adl/p-{}"
# 複数ページに対して情報を取得する
# target_url=url.format(i) for文でiをループする,rangeの数字は実際にページを見て設定した
for i in range(1,10):
    target_url=url.format(i)
    r=requests.get(target_url)
    sleep(1)
    soup= BeautifulSoup(r.text)
    # 大枠で必要な情報を取得する,今回はaタグが大枠
    contents=soup.find_all('li',class_='p-articles-list-item')
    for content in contents:
    # 詳細の情報を取得する
        title=content.find('h2',class_='p-item-title').text
        price=content.find('div',class_='p-item-most-important').text
        tag=content.find('div',class_='p-item-supplementary-info').text
        detail=content.find('div',class_='p-item-detail').text
        # date,onsale(更新日,受付終了)は、タグで取得できない場合に処理が止まるので、条件分岐する
        if content.find('div',class_='u-margin-xs-b')==None:
            date='0'
        else:
            date=content.find('div',class_='u-margin-xs-b').text
        if content.find('div',class_='p-item-close-text')==None:
            onsale=''
        else:
            onsale=content.find('div',class_='p-item-close-text').text
        # 辞書型のリストに格納し、後でcsvに変換しやすくする
        d={
            'title':title,
            'price':price,
            'tag':tag,
            'detail':detail,
            'date':date,
            'onsale':onsale
        }
        d_list.append(d)
# print(d_list)
# 取得したデータをcsvにするには、いったん表形式(データフレーム)に変換する必要がある,辞書型ならできる
# df.head()で先頭5つの確認、df.shapeで表の大きさを確認することもできる
df=pd.DataFrame(d_list)
df.to_csv('test.csv',index=None,encoding='utf-8-sig')