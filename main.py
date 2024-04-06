from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from forms.user import RegisterForm
from data.pet import Pet
from data.post import Post
from forms.login import LoginForm
from forms.pets import PetForm
from forms.posts import PostForm
from flask_login import LoginManager, login_user, current_user
import json
from geopy import Nominatim
import requests
'''
< div


class ="photo_pet" >

< img
src = "" >
< / div >
'''
app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'pets.website_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def get_coords(city, country):
    app = Nominatim(user_agent="PetWeb")
    location = app.geocode(f"{country}, {city}").raw
    return location


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        city = current_user.city
    else:
        city = 'Москва'
    return render_template('index.html', title='Главная', city=city)


@app.route('/category')
def category():
    return render_template('category.html', title='Категории')


@app.route('/organizations')
def organizations():
    f = open('organizations.json', encoding="utf8")
    r = json.load(f)
    tit, names, im, texts = [], [], [], []
    for key in r:
        tit.append(key)
        names.append(r[key]["name"])
        im.append(r[key]["img"])
        texts.append(r[key]["text"])
    return render_template('organizations.html', title='Организации', name=names, types=tit, img=im, text=texts)


@app.route('/organizations/<types>')
def organization(types):
    f = open('organizations.json', encoding="utf8")
    r = json.load(f)
    n = r[types]["name"]
    if current_user.is_authenticated:
        city = current_user.city
    else:
        city = 'Москва'
    src = r[types]["src"]
    return render_template('org_type.html', title=n, name=n, city=city, link_kard=src)


@app.route('/add_post')
def add_post():
    if current_user.is_authenticated:
        form1 = PostForm()
        form2 = PetForm()
        if form1.validate_on_submit() and form2.validate():
            post = Post()
            pet = Pet()
            post.pet = pet.id
            post.user_id = current_user.id
            pet.post_id = post.id
            db_sess = db_session.create_session()
            db_sess.add(post)
            db_sess.add(pet)
            db_sess.commit()
        return render_template('add_post.html', title='Создание объявления', form1=form1, form2=form2)


@app.route('/choice_city')
def choice_city():
    n = "Выбор города"
    if current_user.is_authenticated:
        city = current_user.city
    else:
        city = 'Москва'
    return render_template('choice_city.html', title=n, city=city)


@app.route('/category/<types>')
def subcategory(types):
    f = open('category.json', encoding="utf8")
    r = json.load(f)
    if types in r:
        m = r[f"{types}"]['types']
        name = r[f"{types}"]['name']
        return render_template('subcategory.html', title=str(types), name=name, types=m)


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        city = 'Суругт'
        return render_template('profile.html', title='Профиль', city=city)
    return render_template('autorization.html', title='Авторизация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('profile.html')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/profile")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('profile.html')
    form = RegisterForm()
    if form.validate_on_submit():
        if len(form.password.data) < 6:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Минимальная длина пароля: 6")
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Почта телефона уже используется")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/profile")
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/pets.db")
    app.run(port=8080, host='127.0.0.1')
