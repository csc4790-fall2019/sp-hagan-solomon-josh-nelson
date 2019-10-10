from flask import Flask, url_for, render_template, request
from werkzeug.utils import redirect
import json
from pathlib import Path

import json
from pathlib import Path

app = Flask(__name__)


@app.route('/<name>')
def index(name):
    url_for('static', filename='style1.css')
    return '<h1>hello {}!<h1>'.format(name)


@app.route('/login/welcomepage')
def welcome_page():
    url_for('static', filename='style1.css')
    return render_template('template1.html', name='/login/welcomepage')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['passwowrd'] != 'admin':
            error = 'Invalid Credentials. Please Try Again'
        else:
            return redirect(url_for('login/welcompage'))
    return render_template('login_template.html', error=error)


@app.route('/register/reg', methods=['POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            create_login(request.form['username'], request.form['password'])
            error = 'Invalid Credentials. Please Try Again'
        else:
            return redirect(url_for('login/welcome_page'))
    return render_template('register_template.html', error=error)

def create_login(username, password):
    cred_folder = Path('credentials')
    cred_path = cred_folder
    if not Path(cred_path).exists():
        Path(cred_path).mkdir(parents=True)
        cred = {}
        cred['title'] = hash(username)
        cred["score"] = hash(password)

        with open(cred_path / (hash(username) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(cred, file)

if __name__ == '__main__':
    app.run()
