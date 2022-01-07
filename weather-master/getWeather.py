
import urllib.request
from bs4 import BeautifulSoup
import requests

#アイコンが格納されているパス（絶対パスで入力）
iconPath = "/Users/kodaishiotsuki/Desktop/weather-master/img/"
#トークンID
lineNotifyToken = ''
#LINE Notify APIのURL
lineNotifyApi = 'https://notify-api.line.me/api/notify'

# 抽出対象のRSSとURL(福岡県福岡市)
# 以下のリンクを参照して自身の天気を確認
# @link https://weather.yahoo.co.jp/weather/rss/
rssUrl = "https://rss-weather.yahoo.co.jp/rss/days/8210.xml"
URL = "https://weather.yahoo.co.jp/weather/jp/40/8210/40133.html"

# 探索したいキーワード
keyword = '福岡'
# 取得したい天気の件数
perDay = 2

# 天気に関するタイトルリスト
titleList = []
# 天気に関する詳細リスト
descList = []

## parser : 天気情報WebページのHTMLタグから天気情報を抽出してパースするメソッド ##
#yahoo側がRSS配信にて提供している天気予報情報を呼び出し取得
def parser(rssUrl):
    with urllib.request.urlopen(rssUrl) as res:
        xml = res.read()
        soup = BeautifulSoup(xml, "html.parser")
        #取得したデータの中からタイトル、説明文を取り出す
        for item in soup.find_all("item"):
            title = item.find("title").string
            description = item.find("description").string
            #引数には検索する文字列を指定。見つからなかった場合は -1 を返す。
            if title.find(keyword) != -1:
                # 配列に格納
                titleList.append(title)
                descList.append(description)


## ckWeather : 取得した天気情報とそれに応じた天気アイコンを出力するメソッド ##
# 上記で取得した説明文情報(descList)を参照
def ckWeather(detail):
    #isFind定数をフラグにする 画像が見つかったらTrue,見つからなかったらFalse
    isFind = False

    # 説明文に合致する画像を探し出す(例：晴れなら晴れの画像)
    # boolean,fileNameを用意
    # boolean→true or false
    # fileName→画像path
    for boolean, fileName in [
        [detail.find("晴") != -1 and (detail.find("曇")) == -1 and (detail.find("雨")) == -1 and (detail.find("雪")) == -1, "sunny.png"],
        [detail.find("晴一時曇") != -1 or (detail.find("晴のち曇")) != -1 or (detail.find("晴時々曇")) != -1, "sunnyToCloud.png"],
        [detail.find("晴一時雨") != -1 or (detail.find("晴のち雨")) != -1 or (detail.find("晴時々雨")), "sunnyToRain.jpg"],
        [detail.find("晴一時雪") != -1 or (detail.find("晴のち雪")) != -1 or (detail.find("晴時々雪")) != -1, "sunnyToSnow.jpg"],
        [detail.find("曇") != -1 and (detail.find("晴")) == -1 and (detail.find("雨")) == -1 and (detail.find("雪")) == -1, "cloud.png"],
        [detail.find("曇一時晴") != -1 or (detail.find("曇のち晴")) != -1 or (detail.find("曇時々晴")) != -1, "cloudToSunny.png"],
        [detail.find("曇一時雨") != -1 or (detail.find("曇のち雨")) != -1 or (detail.find("曇時々雨")) != -1, "cloudToRain.png"],
        [detail.find("曇一時雪") != -1 or (detail.find("曇のち雪")) != -1 or (detail.find("曇時々雪")) != -1, "cloudToSnow.jpg"],
        [detail.find("雨") != -1 and (detail.find("晴")) == -1 and (detail.find("曇")) == -1 and (detail.find("雪")) == -1, "rain.png"],
        [detail.find("雨一時晴") != -1 or (detail.find("雨のち晴")) != -1 or (detail.find("雨時々晴")) != -1, "rainToSunny.jpg"],
        [detail.find("雨一時曇") != -1 or (detail.find("雨のち曇")) != -1 or (detail.find("雨時々曇")) != -1, "rainToCloud.png"],
        [detail.find("雨一時雪") != -1 or (detail.find("雨のち雪")) != -1 or (detail.find("雨時々雪")) != -1, "rainToSnow.png"],
        [detail.find("雪") != -1 and (detail.find("晴")) == -1 and (detail.find("雨")) == -1 and (detail.find("曇")) == -1, "snow.png"],
        [detail.find("雪一時晴") != -1 or (detail.find("雪のち晴")) != -1 or (detail.find("雪時々晴")) != -1, "snowToSunny.jpg"],
        [detail.find("雪一時曇") != -1 or (detail.find("雪のち曇")) != -1 or (detail.find("雪時々曇")) != -1, "snowToCloud.jpg"],
        [detail.find("雪一時雨") != -1 or (detail.find("雪のち雨")) != -1 or (detail.find("雪時々雨")) != -1, "snowToRain.jpg"],
        [detail.find("暴風雨") == -1, "typhon.png"],
        [detail.find("暴風雪") == -1, "heavySnow.jpg"],
    ]:
        # 合致する画像が存在するとき、該当する画像ファイルを添付してLINE通知
        if boolean: #合致する画像が存在
            # バイナリーデータで読み込む(コンピュータが読み取れるように0と1の値で書かれたデータのこと)
            # open(読み込むファイル,読み込み専用バイナリーデータ)
            binary = open(iconPath + fileName, mode='rb')
            files = {'imageFile': binary}
            #LINEに通知を送る
            requests.post(lineNotifyApi, data=payload, headers=headers, files=files)
            #isFind定数をTrueに変更
            isFind = True
            break
    # 画像が存在しない場合は、画像ファイルなしでLINE通知
    if not isFind:
        requests.post(lineNotifyApi, data=payload, headers=headers)


## メイン処理 ###################################################################################

# 天気予報サイトのHTMLタグから天気情報を抽出
parser(rssUrl)
for i in range(0, perDay):

    # 情報を辞書型にする
    # 通知したい内容
    payload = {'message': "\n" + titleList[i]}
    # 認証情報
    headers = {'Authorization': 'Bearer ' + lineNotifyToken}

    # 天気情報とそれに応じた天気アイコンを出力
    ckWeather(descList[i])

# yahoo天気予報のURL情報
payload = {'message': URL}
headers = {'Authorization': 'Bearer ' + lineNotifyToken}
requests.post(lineNotifyApi, data=payload, headers=headers)

################################################################################################
