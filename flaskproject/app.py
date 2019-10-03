from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def index(name):
    return '<h1>hello {}!<h1>'.format(name)

@app.route('/welcome')
def welcome_page:
    return '<h1>this is our welcome page {}!<h1>'


if __name__ == '__main__':
    app.run()
