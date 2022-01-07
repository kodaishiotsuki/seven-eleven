import requests
import datetime
import pytz

##-----日時を取得-----#
time = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
#見やすい形に変換
time = time.strftime('%Y年%m月%d日 %H:%M:%S')
# print(time)


# LINE_Notify_APIのURL
api_url = 'https://notify-api.line.me/api/notify'
# 取得したトークン
token = ''
# 時刻を送る内容の変数に設定
send_contents = time

# 情報を辞書型にする
token_dic = {'Authorization': 'Bearer' + ' ' + token}  # 認証情報
send_dic = {'message': send_contents}  # 送りたい内容

# LINEに通知を送る(self.access_token(アクセスするWEB AIPのURL,認証情報,送りたい内容))
# requests.post(api_url, headers=token_dic, data=send_dic)


##-----LINEに画像を送信する方法-----##
# 画像ファイルパスを指定(png/jpgのみ)
image_file = './img/fwj.png'
# バイナリーデータで読み込む(コンピュータが読み取れるように0と1の値で書かれたデータのこと)
# open(読み込むファイル,読み込み専用バイナリーデータ)
binary = open(image_file, mode='rb')
# 指定の辞書型にする(imageFileはAPIの決まり)
image_dic = {'imageFile': binary}
# LINEに画像とメッセージを送る
# requests.post(api_url, headers=token_dic, data=send_dic, files=image_dic)



