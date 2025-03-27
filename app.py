from flask import Flask, request, render_template, redirect, url_for, send_file
import requests
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FILE = "valid_usernames.txt"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def validate_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['code'] == 0  # Trả về True nếu username hợp lệ
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.txt'):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            valid_usernames = []
            with open(file_path, 'r') as f:
                usernames = f.read().splitlines()
                for username in usernames:
                    if validate_username(username):
                        valid_usernames.append(username)
            
            with open(RESULT_FILE, 'w') as f:
                f.write('\n'.join(valid_usernames))
            
            return redirect(url_for('download_file'))
        else:
            return "Invalid file format! Please upload a .txt file."
    return render_template('index.html')

@app.route('/download')
def download_file():
    return send_file(RESULT_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)