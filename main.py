from flask import Flask, render_template
from data import db_session
from data.users import User

app = Flask(__name__, static_folder="static")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    db_session.global_init("db/pets.db")
    app.run(port=8080, host='127.0.0.1')