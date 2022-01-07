import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import re

# csvの読み込み
df=pd.read_csv('./test.csv')

# re.sub(置換前、置換後、置換対象)で複数の対象を置換する replaceは1つだけ置換
# csvに含まれる不要な文字列を除去し、int型にする
for i in range(len(df)):
    df.price[i] = int(re.sub(r"[\n,円]", "", df.price[i]))
# print(df.price[1:10])

# 階級の範囲の設定
df.price.hist(bins=100)

# ラベル表示,デフォルトだと日本語は文字化する
plt.title("アルコール類の価格帯")
plt.xlabel("金額(円)")
plt.ylabel("度数(出現頻度)")

plt.savefig('price_bins.png')

plt.show()