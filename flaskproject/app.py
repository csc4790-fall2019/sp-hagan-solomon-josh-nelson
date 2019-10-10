from flask import Flask, url_for, render_template, request
from werkzeug.utils import redirect

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
        if request.form['username'] !='admin' or request.form['passwowrd'] != 'admin':
            error = 'Invalid Credentials. Please Try Again'
        else:
            return redirect(url_for('login/welcompage'))
    return render_template('login_template.html', error=error)

@app.route('register', methods=['POST'])
def register():
    error = None
    #if request.method == 'POST':



if __name__ == '__main__':
    app.run()
