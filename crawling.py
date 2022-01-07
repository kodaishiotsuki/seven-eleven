from time import sleep
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# このパスは個人ごとに書き換える必要があります
chrome_path='/Users/kodaishiotsuki/Desktop/SevenEleven/chromedriver'

options = Options()
options.add_argument('--incognito')

driver = webdriver.Chrome(executable_path=chrome_path, options=options)

url='https://search.yahoo.co.jp/image'
driver.get(url)

sleep(3)

query ='呪術廻戦'
search_box=driver.find_element_by_class_name('SearchBox__searchInput')
search_box.send_keys(query)
search_box.submit()

sleep(3)

# ()の中はjsのcodeを書く,ややこしいのでマネして書こう
height=1000
while height < 1300:
    driver.execute_script("window.scrollTo(0,{});".format(height))
    height+=100
    sleep(1)

# 画像の要素を選択する
# element's'にすることで、一つだけで終わらないようにする
elements= driver.find_elements_by_class_name('sw-Thumbnail')

d_list=[]
# 要素からurlを取得する,番号も一緒に出したいのでemunerateを使う,defは0からstartなので1にする
for i,element in enumerate(elements,start=1):
    name =f'{query}_{i}'
    raw_url=element.find_element_by_class_name('sw-ThumbnailGrid__domain').text
    yahoo_image_url=element.find_element_by_tag_name('img').get_attribute('src')
    title=element.find_element_by_class_name('sw-ThumbnailGrid__title').text

    d={
        'filename':name,
        'raw_url':raw_url,
        'yahoo_image_url':yahoo_image_url,
        'title':title
    }

    d_list.append(d)

    sleep(2)

df=pd.DataFrame(d_list)
df.to_csv('image_urls_20220103.csv')
driver.quit()

