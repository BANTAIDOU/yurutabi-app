from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret-key"  # セッションやflash用

# データベースの初期化
DB_NAME = "users.db"

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
        conn.commit()
        conn.close()

init_db()

# トップページ
@app.route('/')
def index():
    return render_template('index.html')

# サインアップ
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("登録成功！ログインしてください。")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("そのユーザー名は既に使われています。")
    return render_template('signup.html')

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            flash(f"{username}さん、ログイン成功！")
            return redirect(url_for('index'))
        else:
            flash("ログイン失敗。ユーザー名またはパスワードが違います。")
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
