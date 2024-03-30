from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/autorization')
def autoriz():
    return render_template('autorization.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.phone == form.phone.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Номер телефона уже используется")
        user = User(
            name=form.name.data,
            phone=form.phone.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/profile')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/pets.db")
    app.run(port=8080, host='127.0.0.1')
