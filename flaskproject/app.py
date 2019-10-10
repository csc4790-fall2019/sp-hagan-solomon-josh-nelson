from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/<name>')
def index(name):
    url_for('static', filename='style1.css')
    return '<h1>hello {}!<h1>'.format(name)

@app.route('/login/welcomepage')
def welcome_page():
    url_for('static', filename='style1.css')
    return render_template('template1.html', name='/login/welcomepage')


if __name__ == '__main__':
    app.run()
