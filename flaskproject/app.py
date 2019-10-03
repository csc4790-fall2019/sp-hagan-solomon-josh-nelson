from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def index(name):
    return '<h1>hello {}!<h1>'.format(name)


if __name__ == '__main__':
    app.run()
