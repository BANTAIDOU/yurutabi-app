from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "yurutabi-secret-key"

USERS_FILE = "users.json"

# ---------------- ユーザーデータの管理 ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# ---------------- ルーティング ----------------
@app.route("/")
def index():
    username = session.get("username")
    users = load_users()
    favorites = users.get(username, {}).get("favorites", []) if username else []
    return render_template("index.html", username=username, favorites=favorites)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return "ログイン失敗しました"
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        if username in users:
            return "そのユーザー名は既に使われています"
        users[username] = {"password": password, "favorites": []}
        save_users(users)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    if "username" not in session:
        return redirect(url_for("login"))

    map_name = request.form["map_name"]
    users = load_users()
    username = session["username"]

    if map_name not in users[username]["favorites"]:
        users[username]["favorites"].append(map_name)
        save_users(users)

    return redirect(url_for("index"))

# ---------------- メイン ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
