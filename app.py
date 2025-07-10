import os
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

UPLOAD_FOLDER = 'static/uploaded_files'

# Flask アプリ初期化
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理のために必要
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 必要なフォルダがなければ作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask-Login 設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 仮ユーザー情報
users = {'user1': {'password': 'password123'}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# ===== ルーティング =====

# ログイン画面
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

# ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# トップページ（ファイル一覧）
@app.route('/')
@login_required
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

# ファイルアップロード
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
        return redirect('/')
    return render_template('upload.html')

# ファイルダウンロード
@app.route('/files/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ===== アプリ起動 =====
if __name__ == '__main__':
    app.run(debug=True)
