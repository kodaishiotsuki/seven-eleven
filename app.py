from datetime import datetime,date
from flask import Flask, render_template, redirect, request,url_for
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 意外と重要w
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


# top
@app.route('/', methods=['GET', 'POST'])  # get,postどちらも取得できるように設定
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()  # 投稿全部を取り出す
        # postsをindex.htmlと一緒に渡す
        return render_template('index.html', posts=posts, today=date.today())
    else:  # formから送られた内容を受け取る(POSTの場合)
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        due = datetime.strptime(due, '%Y-%m-%d')  # 文字型を解消
        new_post = Post(title=title, detail=detail,
                        due=due)  # formからの投稿を新投稿として定義

        # DBに保存
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')  # TOPページに遷移


# Create
@app.route('/create')
def create():
    return render_template('create.html')


# detail
@app.route('/detail/<int:id>')  # そのidに属しているpostを取得
def read(id):  # read関数にidを忘れずに！
    post = Post.query.get(id)  # DBから指定したidの投稿を取り出す
    return render_template('detail.html', post=post)


# update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):  # update関数にidを忘れずに！
    post = Post.query.get(id)  # DBから指定したidの投稿を取り出す
    if request.method == 'GET':
        # updateのページ
        # もともと入っていた値が格納されるためにpost=post
        return render_template('update.html', post=post)
    else:
        # DBに反映
        # formタグのtitleを取得しpostのtitleに反映させる
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()

        # TOPに遷移
        return redirect('/')


# delete
@app.route('/delete/<int:id>')  # そのidに属しているpostを取得
def delete(id):  # delete関数にidを忘れずに！
    post = Post.query.get(id)  # DBから指定したidの投稿を取り出す

    db.session.delete(post)  # DBの内容削除（保存はadd + commit）
    db.session.commit()
    return redirect('/')

# おみくじページへの遷移
@app.route('/fortune-teller')
def fortune():
    return render_template('fortune-teller.html')

# おみくじをやって、結果を返す
@app.route('/teller')
def teller():
    fortune = {
    '大吉': '清水の舞台から飛び降りても無傷なレベル',
    '中吉': '間違いなく棚からぼた餅が落ちてくるレベル',
    '小吉': '長い物には巻かれた方がいいレベル',
    '末吉': '地獄の沙汰も金次第なレベル',
    '凶': '大凶よりはマシというレベル',
    '大凶': '占い師も口をつぐむレベル'
    }
    luck, advice = random.choice(list(fortune.items()))
    return render_template('fortune-teller.html',luck=luck, advice=advice)


if __name__ == '__main__':
    app.run()
