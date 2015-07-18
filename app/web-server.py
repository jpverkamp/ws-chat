import flask

app = flask.Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000)
