from flask import Flask, render_template, request, redirect, send_from_directory
import os

app = Flask(__name__)

# アップロード先のフォルダ（保存場所）
UPLOAD_FOLDER = 'static/uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# トップページ：アップロード済みのファイル一覧を表示
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)  # 保存フォルダ内のファイル一覧を取得
    return render_template('index.html', files=files)

# ファイルアップロードの処理
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']  # フォームからアップロードされたファイルを取得
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)  # 保存
        return redirect('/')  # アップロード後トップに戻る
    return render_template('upload.html')  # アップロード画面を表示

# ファイルダウンロードの処理
@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# アプリ起動
if __name__ == '__main__':
    # フォルダが存在しない場合は作る
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # アプリを起動（デバッグモード）
    app.run(debug=True)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 仮のユーザーデータ
users = {'user1': {'password': 'password123'}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect('/')
        return 'ログイン失敗'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
