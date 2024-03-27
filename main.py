from flask import Flask, render_template

app = Flask(__name__, static_folder="static")

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')