# ライブラリのインポート
import os
from time import sleep

import pandas as pd
import requests

IMAGE_DIR='./images/'

#CSVの読み込み
df=pd.read_csv('image_urls_20220103.csv')

if os.path.isdir(IMAGE_DIR):
    print('既にあります')
else:
    os.makedirs(IMAGE_DIR)


# 画像の保存,一度に2つのものを取り出すためにzipでまとめる
for file_name, yahoo_image_url in zip(df.filename[:5],df.yahoo_image_url[:5]):
    image=requests.get(yahoo_image_url)
    # wb write binaryこれにより画像の保存が可能になる,fはfile
    with open(IMAGE_DIR+file_name+'.jpg','wb') as f:
        f.write(image.content)
    
    sleep(2)
    # os フォルダに画像を保存するため

