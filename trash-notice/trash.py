import requests
import datetime
import locale
import schedule
import time


# Line_Notifyへメッセージ、画像、スタンプを送信するプログラム
class LINE_Notify:
    def __init__(self):
        # LINE_Notify_APIのURL
        self.api_url = 'https://notify-api.line.me/api/notify'
        # 取得したトークン
        self.token = ''
        # 認証情報
        self.headers = {'Authorization': 'Bearer' + ' ' + self.token}

    # メッセージのみ送信する関数
    def Sent_Message(self, message):
        # 送りたい内容
        payload = {'message': message}

        # LINEに通知を送る
        # requests.post(API URL,認証情報,送りたい内容)
        requests.post(self.api_url, headers=self.headers, params=payload)

    # メッセージと画像を送信するための関数
    def Sent_Image(self, message, image):
        # 送りたい内容
        payload = {'message': message}

        # 画像
        # バイナリーデータで読み込む(コンピュータが読み取れるように0と1の値で書かれたデータのこと)
        # open(読み込むファイル,読み込み専用バイナリーデータ)
        binary = open(image, mode='rb')
        # 指定の辞書型にする(imageFileはAPIの決まり)
        files = {'imageFile': binary}

        # LINEに通知を送る
        # requests.post(API URL,認証情報,送りたい内容,送りたい画像)
        requests.post(self.api_url, headers=self.headers,params=payload, files=files)

    # メッセージとスタンプを送信するための関数
    def Sent_Stamp(self, message, stamp_number):
        # 送りたい内容
        payload = {
            'message': message,
            'stickerPackageId': 1,
            'stickerId': stamp_number
        }

        # LINEに通知を送る
        # requests.post(API URL,認証情報,送りたい内容)
        requests.post(self.api_url, headers=self.headers, params=payload)


# 本日の日付、曜日、メッセージを出力するプログラムをdefで関数化
def Gomi_Sute_Message():
    # localeモジュールでロケールを変更する。日本のローカル情報を取得。コピペでOK
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    # datetimeモジュールのnow関数で今日の日付を取得
    today = datetime.datetime.now()
    # weekday関数で曜日を取得(0=月,1=火,2=水,3=木,4=金,5=土,6=日)
    week_num = today.weekday()
    # Weekday関数の返り値は数値なので、曜日のリストをあわせて準備
    week_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
    # 今日の日付、週の値、曜日の書き出し
    # print(today, week_num, week_list[week_num])

    #可燃ゴミの日→毎週火曜、金曜
    # 月曜日(week_num= 0)と木曜日(week_num= 3)に翌日の可燃ごみのメッセージ
    if week_num == 0 or week_num == 3:
        message = f'\n今日は'+ week_list[week_num] + 'です.\n明日は可燃ゴミの日です🚮'
        image_path = './img/gomi_mark01_moeru.png'

    #不燃ゴミの日→2回目の木曜日
    # 第2水曜日(week_num=2)の翌日に不燃ゴミのメッセージ
    elif week_num == 2:
        message = f'\n今日は'+ week_list[week_num] + \
            'です。\n明日が第2木曜日なら不燃ゴミの日です🚮'
        image_path = './img/gomi_mark02_moenai.png'


    # 第4金曜日(week_num=4)の翌日に資源ゴミのメッセージ
    elif week_num == 4:
        message = f'\n今日は'+ week_list[week_num] + \
            'です。\n明日が第4土曜日なら資源ゴミの日です🚮'
        image_path = './img/gomi_mark05_petbottle.png'

    # それ以外の日は、ゴミ捨てがないメッセージ
    else:
        message = f'\n今日は'+ week_list[week_num] + 'です。\n明日のゴミ捨てはありません🚯'
        image_path = './img/ダウンロード.jpeg'

    # print(week_list[week_num], message)
    # returnで曜日ごのメッセージと画像を返り値として設定
    return message, image_path


# # 定期的に実行したいメインのプログラム
# def main():
#     LINE_Notify = LINE_Notify()
#     # Gomi_Sute_Message関数からメッセージと画像パスを取得する
#     message, image_path = Gomi_Sute_Message()
#     # Sent_Image関数でメッセージと画像を送ります。
#     LINE_Notify.Sent_Image(message, image_path)


# if __name__ == '__main__':
#     # shedleモジュールで毎日22:00にmain関数を実行します。
#     schedule.every().day.at("22:00").do(main)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# プログラムの実行
if __name__ == '__main__':
    # インスタンスを生成
    LINE_Notify = LINE_Notify()
    # メッセージ送信を実行。関数の引数として（）内にメッセージを入れる
    # LINE_Notify.Sent_Message('hogehogehogehoge')
    # メッセージ,画像送信を実行。関数の引数として（）内にメッセージ、画像のパスを入れる
    message, image_path = Gomi_Sute_Message()
    LINE_Notify.Sent_Image(message, image_path)
    # メッセージ,スタンプ送信を実行。関数の引数として（）内にメッセージ、スタンプIDを入れる
    # LINE_Notify.Sent_Stamp('stamp',10) #第2引数の番号を変えるとスタンプ変更
