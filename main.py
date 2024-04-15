from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from forms.user import RegisterForm
from data.post import Post
from forms.login import LoginForm
from forms.posts import PostForm
from flask_login import LoginManager, login_user, current_user
import json
import os
import requests
from PIL import Image

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'pets.website_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        city = current_user.city
    else:
        city = 'Москва'
    db_sess = db_session.create_session()
    p = ''
    if request.method == 'POST':
        pass
        # p = db_sess.query(Post).filter(Post.category == form.category.data).all()
    else:
        p = db_sess.query(Post).order_by(Post.created_date.desc()).limit(50).all()
    for i in range(len(p)):
        if len(p[i].content) >= 50:
            p[i].content = p[i].content[:50] + '...'
    return render_template('index.html', title='Главная', city=city, posts=p)


@app.route('/post/<ipost>', methods=['GET', 'POST'])
def index_post(ipost):
    db_sess = db_session.create_session()
    p = db_sess.query(Post).filter(Post.id == ipost).first()
    try:
        t = p.title
    except:
        t = ''
    if os.path.exists('C:/Users/Сергей/Desktop/pets/static/pets_photo/' + p.photo.split('/')[3] + '/map.png') == 0:
        img = None
    else:
        img = '/static/pets_photo/' + p.photo.split('/')[3] + '/map.png'
    user = db_sess.query(User).filter(User.id == p.user_id).first()
    with open('category.json', encoding="utf8") as f:
        r = json.load(f)
        c = r[p.category]["name"]
    a = str(p.age)
    return render_template('view_post.html', title=t, post=p, img=img, user=user, a=a, c=c)


@app.route('/category')
def category():
    f = open('category.json', encoding="utf8")
    r = json.load(f)
    m = []
    for i in r:
        if r[i]["types"]:
            m.append([r[i]["name"], i, r[i]["src"]])
    return render_template('category.html', title='Категории', m=m, )


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
    m = []
    n = r[types]["name"]
    response = requests.get(
        f'https://search-maps.yandex.ru/v1/?text={n} {current_user.city}&type=biz&results=1&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
    if response:
        json_response = response.json()
        for i in json_response["features"]:
            print(json_response)
            i = i["properties"]
            m.append([i["CompanyMetaData"]["name"], i["CompanyMetaData"]["address"],
                   i["CompanyMetaData"]["url"], i["CompanyMetaData"]["Hours"]["text"], [i["CompanyMetaData"]["Phones"][j]["formatted"] for j in range(len(i["CompanyMetaData"]["Phones"]))]])
    if current_user.is_authenticated:
        city = current_user.city
    else:
        city = 'Москва'
    src = r[types]["src"]
    return render_template('org_type.html', title=n, name=n, city=city, link_kard=src, info=m)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if current_user.is_authenticated:
        form = PostForm()
        if request.method == 'POST' or form.validate_on_submit():
            if form.age.data < 0:
                return render_template('add_post.html', title='Создание объявления', form=form,
                                       age_err="Введен неверный возраст")

            with open('category.json', 'r', encoding="utf8") as f:
                r = json.load(f)
                if form.breed.data not in r[form.category.data]["types"]:
                    r[form.category.data]["types"].append(form.breed.data)
            with open('category.json', 'w', encoding="utf8") as f:
                json.dump(r, f, ensure_ascii=False)
            db_sess = db_session.create_session()
            count_p = len(db_sess.query(Post).filter(Post.user_id == current_user.id).all()) + 1
            os.makedirs(f'C:/Users/Сергей/Desktop/pets/static/pets_photo/{str(count_p)}', exist_ok=True)
            if form.photo.data.filename != '':
                try:
                    file = Image.open(form.photo.data, mode='r', formats=None)
                    if file:
                        w, h = file.size
                        if w > h:
                            file = file.crop((w - (w - h) // 2 - h, 0, w - (w - h) // 2, h))
                        if w < h:
                            file = file.crop((0, h - (h - w) // 2 - w, w, h - (h - w) // 2))
                        if form.photo.data.filename == 'photo_def.jpg':
                            form.photo.data.filename = 'photo.jpg'
                        file.save(
                            f'C:/Users/Сергей/Desktop/pets/static/pets_photo/{str(count_p)}/{form.photo.data.filename}')
                        ph = f'/static/pets_photo/{str(count_p)}/{form.photo.data.filename}'
                except:
                    pass
            else:
                file = Image.open('C:/Users/Сергей/Desktop/pets/static/img/photo_def.jpg', mode='r', formats=None)
                if file:
                    file.save(
                        f'C:/Users/Сергей/Desktop/pets/static/pets_photo/{str(count_p)}/photo_def.jpg')
                    ph = f'/static/pets_photo/{str(count_p)}/photo_def.jpg'
            if form.address.data:
                response = requests.get(
                    f'https://search-maps.yandex.ru/v1/?text={form.address.data}&type=geo&results=1&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
                if response:
                    json_response = response.json()
                    try:
                        ll1, ll2 = json_response["features"][0]["geometry"]["coordinates"][0], \
                            json_response["features"][0]["geometry"]["coordinates"][1]
                        address = json_response["features"][0]["description"]
                    except:
                        address = ''
                    if address:
                        response = requests.get(
                            f"http://static-maps.yandex.ru/1.x/?ll={ll1},{ll2}&pt={ll1},{ll2},pm2vvl&spn=0.02,0.01&l=map&lang=ru_RU&apikey=b2673b46-1c73-4d52-9bb6-e23eab02974b")
                        if response:
                            map_file = f'C:/Users/Сергей/Desktop/pets/static/pets_photo/{str(count_p)}/map.png'
                            with open(map_file, "wb") as file:
                                file.write(response.content)
            post = Post(
                price=form.price.data,
                phone=form.phone.data,
                photo=ph,
                currency=form.currency.data,
                title=form.title.data,
                content=form.content.data,
                address=address,
                destination=form.destination.data,
                delivery=form.delivery.data,
                user_id=current_user.id,
                breed=form.breed.data,
                color=form.color.data,
                age=form.age.data,
                documents=form.documents.data,
                vaccin=form.vaccin.data,
                steril=form.steril.data,
                category=form.category.data,
            )
            db_sess.add(post)
            db_sess.commit()
            return redirect("/")
        return render_template('add_post.html', title='Создание объявления', form=form)


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
        os.makedirs(f'C:/Users/Сергей/Desktop/pets/static/avatars/{user.id}', exist_ok=True)
        file = Image.open('C:/Users/Сергей/Desktop/pets/static/img/avatar.png', mode='r', formats=None)
        file.save(
            f'C:/Users/Сергей/Desktop/pets/static/avatars/{user.id}/avatar.png')
        user.photo = f'/static/avatars/{user.id}/avatar.png'
        db_sess.commit()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/profile")
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/pets.db")
    app.run(port=8080, host='127.0.0.1')
