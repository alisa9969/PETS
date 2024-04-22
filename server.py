import werkzeug
from flask import Flask, render_template, redirect, request, session
from forms.filter import FilterForm
import shutil
import datetime
from data import db_session
from data.users import User
from data.favorite import Favorite
from forms.user import RegisterForm
from forms.city import CityForm
from data.post import Post
from forms.edit import EditForm
from forms.photo import PhotoForm
from data.organizations import Organizations
from forms.login import LoginForm
from forms.posts import PostForm
from flask_login import LoginManager, login_user, current_user, logout_user
import json
import os
import requests
from PIL import Image

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'pets.website_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=30
)


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
        city = session.get('city')
        if not city:
            session['city'] = 'Москва'
            city = session['city']
    response2 = requests.get(
        f'https://search-maps.yandex.ru/v1/?text={city}&type=geo&results=1&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
    if response2:
        json_response2 = response2.json()
        session[
            'coords'] = [json_response2["features"][0]["geometry"]["coordinates"][0],
                         json_response2["features"][0]["geometry"]["coordinates"][1]]
    if len(city) > 50:
        city = city[:50] + '...'
    db_sess = db_session.create_session()
    p = ''
    ll1, ll2 = float(session['coords'][0]) + 1, float(session['coords'][1]) + 1
    ll3, ll4 = float(session['coords'][0]) - 1, float(session['coords'][1]) - 1
    ord = session.get('order')
    if ord:
        if ord == 'views':
            p = db_sess.query(Post).order_by(Post.views_count).filter(Post.coords1 <= ll1, Post.coords1 >= ll3,
                                                                      Post.coords2 <= ll2,
                                                                      Post.coords2 >= ll4)
        elif ord == 'price1':
            p = db_sess.query(Post).order_by(Post.price).filter(Post.coords1 <= ll1, Post.coords1 >= ll3,
                                                                Post.coords2 <= ll2,
                                                                Post.coords2 >= ll4)
        elif ord == 'price2':
            p = db_sess.query(Post).order_by(Post.price.desc()).filter(Post.coords1 <= ll1, Post.coords1 >= ll3,
                                                                       Post.coords2 <= ll2,
                                                                       Post.coords2 >= ll4)
        elif ord == 'date':
            p = db_sess.query(Post).order_by(Post.created_date.desc()).filter(Post.coords1 <= ll1,
                                                                              Post.coords1 >= ll3,
                                                                              Post.coords2 <= ll2,
                                                                              Post.coords2 >= ll4)
    else:
        p = db_sess.query(Post).order_by(Post.created_date.desc()).filter(Post.coords1 <= ll1, Post.coords1 >= ll3,
                                                                          Post.coords2 <= ll2,
                                                                          Post.coords2 >= ll4)
    try:
        m = session.get('filter')
        if m[0]:
            if 'Все' not in m[0]:
                filt = p.filter(Post.destination.in_(m[0]))
                if filt:
                    p = filt
        if m[1]:
            if 'Все' not in m[1]:
                filt = p.filter(Post.color.in_(m[1]))
                if filt:
                    p = filt
        if m[2]:
            if 'Все' not in m[2]:
                filt = p.filter(Post.category.in_(m[2]))
                if filt:
                    p = filt
        if m[3]:
            filt = p.filter(Post.age <= m[3][0], Post.age >= m[3][1])
            if filt:
                p = filt
        if m[4]:
            filt = p.filter(Post.price <= m[4][0], Post.price >= m[4][1])
            if filt:
                p = filt
        if m[5]:
            filt = p.filter(Post.delivery == 1)
            if filt:
                p = filt
        if m[6]:
            filt = p.filter(Post.delivery == 1)
            if filt:
                p = filt
        if m[7]:
            filt = p.filter(Post.delivery == 1)
            if filt:
                p = filt
        if m[8]:
            filt = p.filter(Post.delivery == 1)
            if filt:
                p = filt
    except:
        pass
    p = p.limit(30).all()
    for i in range(len(p)):
        if len(p[i].content) >= 50:
            p[i].content = p[i].content[:50] + '...'
        if len(p[i].address) >= 50:
            p[i].address = p[i].address[:50] + '...'
    session["link"] = '/'
    session['link2'] = '/'
    return render_template('index.html', title='Главная', city=city, posts=p)


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    form = FilterForm()
    if request.method == 'POST':
        try:
            if request.values['delete']:
                session.pop('filter', None)
                return redirect(session['link'])
        except:
            pass
        c = []
        d = []
        t = []
        if str(form.price1.data).isalnum() or str(form.price2.data).isalnum() or str(form.age.data).isalnum() or str(
                form.age2.data).isalnum():
            return render_template('filter.html', title='Фильтр', message='Неверный формат ввода')
        for i in form.color.data:
            c.append(i)
        for i in form.destination.data:
            d.append(i)
        for i in form.category.data:
            t.append(i)
        m = [d, c, t, [form.age.data, form.age2.data], [form.price1.data, form.price2.data], form.delivery.data,
             form.documents.data, form.vaccin.data, form.steril.data]
        session['filter'] = m
        return redirect(session['link'])
    return render_template('filter.html', title='Фильтр', form=form)


@app.route('/order', methods=['GET', 'POST'])
def sort_post():
    if request.method == "POST":
        session['order'] = request.values['sort']
        return redirect(session['link'])
    return render_template('sort.html', title='Сортировка')


@app.route('/change_password', methods=['GET', 'POST'])
def change_pin():
    if current_user.is_authenticated:
        if request.method == 'POST':
            if request.values['passw2'] == request.values['passw1']:
                pin1 = werkzeug.security.generate_password_hash(request.values['passw2'])
                db_s = db_session.create_session()
                current_user.hashed_password = pin1
                db_s.merge(current_user)
                db_s.commit()
                return render_template('change_pin.html', title='Изменение пароля', mess="Пароль успешно изменен")
            else:
                return render_template('change_pin.html', title='Изменение пароля', mess="Пароли не совпадают")
    return render_template('change_pin.html', title='Изменение пароля')


@app.route('/post/<ipost>', methods=['GET', 'POST'])
def index_post(ipost):
    db_sess = db_session.create_session()
    p = db_sess.query(Post).filter(Post.id == ipost).first()
    try:
        t = p.title
    except:
        t = ''
    if os.path.exists(
            '/'.join(os.getcwd().split('\\')) + '/static/pets_photo/' + p.photo.split('/')[3] + '/map.png') == 0:
        img = None
    else:
        img = '/static/pets_photo/' + p.photo.split('/')[3] + '/map.png'
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == p.user_id).first()
    with open('category.json', encoding="utf8") as f:
        r = json.load(f)
        c = r[p.category]["name"]
    a = str(p.age)
    if user != current_user:
        p.views_count += 1
        db_sess.merge(p)
        db_sess.commit()
    fv = ''
    fav_txt = ''
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        fv = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.post_id == ipost).first()
        if fv:
            fav_txt = 'В избранном'
        else:
            fav_txt = 'В избранное'
    if request.method == "POST":
        for i in request.values:
            if i == 'fav':
                if fv:
                    db_sess.delete(fv)
                    db_sess.commit()
                    db_sess = db_session.create_session()
                    user = db_sess.query(User).filter(User.id == p.user_id).first()
                    return render_template('view_post.html', title=t, post=p, img=img, user=user, a=a, c=c,
                                           back=session["link2"], fvt='В избранное')
                favorites = Favorite(
                    user_id=current_user.id,
                    post_id=p.id
                )
                db_sess = db_session.create_session()
                db_sess.add(favorites)
                db_sess.commit()
                db_sess = db_session.create_session()
                user = db_sess.query(User).filter(User.id == p.user_id).first()
                return render_template('view_post.html', title=t, post=p, img=img, user=user, a=a, c=c,
                                       back=session["link2"], fvt='В избранном')
            else:
                session['link'] = f'/post/{ipost}'
                db_sess.commit()
                return redirect(f'/user/{p.user_id}')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == p.user_id).first()
    return render_template('view_post.html', title=t, post=p, img=img, user=user, a=a, c=c, back=session["link2"],
                           fvt=fav_txt)


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    session['link'] = '/favorites'
    session['link2'] = '/favorites'
    if current_user.is_authenticated:
        if request.method == "POST":
            for i in request.values:
                if i.isdigit():
                    dbs = db_session.create_session()
                    del_p = dbs.query(Favorite).filter(Favorite.user_id == current_user.id,
                                                       Favorite.post_id == int(i)).first()
                    dbs.delete(del_p)
                    dbs.commit()
        posts = []
        db_sess = db_session.create_session()
        favs = db_sess.query(Favorite.post_id).filter(Favorite.user_id == current_user.id).all()
        for i in favs:
            posts.append(db_sess.query(Post).filter(Post.id == i[0]).first())
        posts = list(
            map(lambda x: [x.title, x.destination, x.price, x.currency,
                           x.content[:45] + '...' if len(x.content) > 45 else x.content,
                           x.address[:45] + '...' if len(x.address) > 45 else x.address, x.photo, x.id, x.delivery,
                           x.created_date.strftime('%d.%m.%Y, %H:%M')], posts))
        return render_template('favorites.html', title='Избранное', posts=posts, ln=len(posts),
                               n=int(str(len(posts))[-1]))
    return redirect('/profile')


@app.route('/category')
def category():
    f = open('category.json', encoding="utf8")
    r = json.load(f)
    m = []
    for i in r:
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
    n = r[types]["name"]
    if current_user.is_authenticated:
        city = current_user.city
    else:
        city = session.get('city')
        if not city:
            session['city'] = 'Москва'
    ds = db_session.create_session()
    filt = ds.query(Organizations).filter(Organizations.type == types, Organizations.city == city).all()
    if not filt:
        response = requests.get(
            f'https://search-maps.yandex.ru/v1/?text={n} {city}&type=biz&results=50&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
        if response:
            json_response = response.json()
            for i in json_response["features"]:
                i = i["properties"]["CompanyMetaData"]
                if i["name"] and i["address"] and 'детский' not in i["name"] and "Детский" not in i[
                    "name"] and "несовершеннолетних" not in i["name"] and "Несовершеннолетних" not in i[
                    "name"] and 'детей' not in i["name"]:
                    org = Organizations(
                        name=i["name"],
                        address=i["address"],
                        type=types,
                        city=city
                    )
                    try:
                        org.url = i["url"]
                    except:
                        pass
                    try:
                        org.hours = i["Hours"]["text"]
                    except:
                        pass
                    try:
                        org.contacts = '\n'.join(list(j["formatted"] for j in i["Phones"]))
                    except:
                        pass
                    ds = db_session.create_session()
                    ds.add(org)
                    ds.commit()
    ds = db_session.create_session()
    m = ds.query(Organizations).filter(Organizations.city == city, Organizations.type == types).all()
    src = r[types]["src"]
    session["link"] = f'/organizations/{types}'
    if len(city) > 100:
        city = city[:100] + '...'
    return render_template('org_type.html', title=n, name=n, city=city, link_kard=src, info=m)


@app.route('/organizations/<types>/<id>')
def org(types, id):
    ds = db_session.create_session()
    m = ds.query(Organizations).filter(Organizations.id == id).first()
    return render_template('org.html', info=m, title=m.name)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if current_user.is_authenticated:
        form = PostForm()
        if request.method == 'POST' or form.validate_on_submit():
            if not str(form.age.data).isdigit() or not str(form.price.data).isdigit():
                return render_template('add_post.html', title='Создание объявления', form=form,
                                       message='Неправильный формат ввода')
            if len(str(form.age.data)) > 3:
                try:
                    form.age.data = int(str(form.age.data)[:3])
                except:
                    form.age.data = 0
            if len(str(form.price.data)) > 10:
                try:
                    form.price.data = int(str(form.price.data)[:10])
                except:
                    form.price.data = 0
            with open('category.json', 'r', encoding="utf8") as f:
                r = json.load(f)
                if form.breed.data not in r[form.category.data]["types"]:
                    r[form.category.data]["types"].append(form.breed.data)
            with open('category.json', 'w', encoding="utf8") as f:
                json.dump(r, f, ensure_ascii=False)
            db_sess = db_session.create_session()
            count_p = len(db_sess.query(Post).all()) + 1
            os.makedirs('/'.join(os.getcwd().split('\\')) + f'/static/pets_photo/{str(count_p)}', exist_ok=True)
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
                            '/'.join(os.getcwd().split(
                                '\\')) + f'/static/pets_photo/{str(count_p)}/{form.photo.data.filename}')
                        ph = f'/static/pets_photo/{str(count_p)}/{form.photo.data.filename}'
                except:
                    pass
            else:
                file = Image.open('/'.join(os.getcwd().split('\\')) + '/static/img/photo_def.jpg', mode='r',
                                  formats=None)
                if file:
                    file.save('/'.join(os.getcwd().split('\\')) +
                              f'/static/pets_photo/{str(count_p)}/photo_def.jpg')
                    ph = f'/static/pets_photo/{str(count_p)}/photo_def.jpg'
            if form.address.data:
                response = requests.get(
                    f'https://search-maps.yandex.ru/v1/?text={form.address.data}&type=geo&results=1&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
                if response:
                    json_response = response.json()
                    if json_response["properties"]["ResponseMetaData"]["SearchResponse"]["found"] == 0:
                        response2 = requests.get(
                            f'https://search-maps.yandex.ru/v1/?text={current_user.city}&type=geo&results=1&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
                        if response2:
                            json_response2 = response2.json()
                            ll1, ll2 = json_response2["features"][0]["geometry"]["coordinates"][0], \
                                json_response2["features"][0]["geometry"]["coordinates"][1]
                            address = json_response2["features"][0]["properties"]["GeocoderMetaData"]["text"]
                    else:
                        ll1, ll2 = json_response["features"][0]["geometry"]["coordinates"][0], \
                            json_response["features"][0]["geometry"]["coordinates"][1]
                        address = json_response["features"][0]["properties"]["GeocoderMetaData"]["text"]
                    if address:
                        response = requests.get(
                            f"http://static-maps.yandex.ru/1.x/?ll={ll1},{ll2}&pt={ll1},{ll2},pm2vvl&spn=0.02,0.01&l=map&lang=ru_RU&apikey=b2673b46-1c73-4d52-9bb6-e23eab02974b")
                        if response:
                            map_file = '/'.join(os.getcwd().split('\\')) + f'/static/pets_photo/{str(count_p)}/map.png'
                            with open(map_file, "wb") as file:
                                file.write(response.content)
            post = Post(
                price=abs(form.price.data),
                phone=form.phone.data,
                photo=ph,
                currency=form.currency.data,
                title=form.title.data,
                content=form.content.data,
                address=address,
                coords1=ll1,
                coords2=ll2,
                destination=form.destination.data,
                delivery=form.delivery.data,
                user_id=current_user.id,
                breed=form.breed.data,
                color=form.color.data,
                age=abs(form.age.data),
                documents=form.documents.data,
                vaccin=form.vaccin.data,
                steril=form.steril.data,
                category=form.category.data,
            )
            db_sess.add(post)
            db_sess.commit()
            return redirect("/")
        return render_template('add_post.html', title='Создание объявления', form=form)


@app.route('/choice_city', methods=['GET', 'POST'])
def choice_city():
    n = "Выбор города"
    form = CityForm()
    flag = 0
    if request.method == 'POST':
        response = requests.get(
            f"https://suggest-maps.yandex.ru/v1/suggest?text={form.search.data}&results=10&type=locality,province&apikey=efb15d6d-85bf-40c5-9172-f0d59c105cdd")
        if response:
            json_response = response.json()
            m = []
            try:
                for i in json_response["results"]:
                    if "locality" in i["tags"] or "province" in i["tags"]:
                        try:
                            text = i["title"]["text"]
                        except:
                            text = ''
                        try:
                            stext = i["subtitle"]["text"]
                        except:
                            stext = ''
                        if text:
                            if stext:
                                m.append(f'{i["title"]["text"]}, {i["subtitle"]["text"]}')
                            else:
                                m.append(f'{i["title"]["text"]}')
                        for ch in m:
                            if ch not in form.city.choices:
                                form.city.choices.append(ch)
                            flag = 1
            except:
                error = 'Ничего не найдено'
                return render_template('choice_city.html', title=n, form=form, error=error, flag=0)
        if form.city.data:
            if current_user.is_authenticated:
                db_sess = db_session.create_session()
                current_user.city = form.city.data
                response2 = requests.get(
                    f'https://search-maps.yandex.ru/v1/?text={form.city.data}&type=geo&results=1&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
                if response2:
                    json_response2 = response2.json()
                    session[
                        'coords'] = [json_response2["features"][0]["geometry"]["coordinates"][0],
                                     json_response2["features"][0]["geometry"]["coordinates"][1]]
                    db_sess.merge(current_user)
                db_sess.commit()
            else:
                session['city'] = form.city.data
            return redirect(session["link"])
    return render_template('choice_city.html', title=n, form=form, error='', flag=flag, cancel=session["link"])


@app.route('/category/<types>/posts')
def posts(types):
    dbs = db_session.create_session()
    session["link"] = f"/category/{types}/posts"
    if current_user.is_authenticated:
        city = current_user.city
    else:
        if not session.get('city'):
            session['city'] = 'Москва'
        city = session.get('city')
    response2 = requests.get(
        f'https://search-maps.yandex.ru/v1/?text={city}&type=geo&results=1&lang=ru_RU&apikey=2c36664f-f6e2-4bc1-9042-306afc19c9fa')
    if response2:
        json_response2 = response2.json()
        session['coords'] = [json_response2["features"][0]["geometry"]["coordinates"][0],
                             json_response2["features"][0]["geometry"]["coordinates"][1]]
    ll1, ll2 = float(session["coords"][0]) - 1, float(session["coords"][0]) + 1
    ll3, ll4 = float(session["coords"][1]) - 1, float(session["coords"][1]) + 1
    categ = session.get("categories")
    if 'all' not in categ:
        posts = dbs.query(Post).filter(Post.category == types, Post.breed.in_(categ))
    else:
        posts = dbs.query(Post).filter(Post.category == types)
    ord = session.get('order')
    if ord:
        if ord == 'views':
            p = posts.order_by(Post.views_count).filter(Post.coords1 <= ll2, Post.coords1 >= ll1,
                                                        Post.coords2 <= ll4,
                                                        Post.coords2 >= ll2)
        elif ord == 'price1':
            p = posts.order_by(Post.price).filter(Post.coords1 <= ll2, Post.coords1 >= ll1,
                                                  Post.coords2 <= ll4,
                                                  Post.coords2 >= ll2)
        elif ord == 'price2':
            p = posts.order_by(Post.price.desc()).filter(Post.coords1 <= ll2, Post.coords1 >= ll1,
                                                         Post.coords2 <= ll4,
                                                         Post.coords2 >= ll2)
        elif ord == 'date':
            p = posts.order_by(Post.created_date.desc()).filter(Post.coords1 <= ll2, Post.coords1 >= ll1,
                                                                Post.coords2 <= ll4,
                                                                Post.coords2 >= ll2)
    else:
        p = posts.order_by(Post.created_date.desc()).filter(Post.coords1 <= ll2, Post.coords1 >= ll1,
                                                            Post.coords2 <= ll4,
                                                            Post.coords2 >= ll2)
    m = session.get('filter')
    try:
        if m['age1']:
            if m['age2']:
                p = p.filter(Post.age >= int(m['age1']), Post.age <= int(m['age2']))
            else:
                p = p.filter(Post.age >= int(m['age1']))
        elif m['age2']:
            p = p.filter(Post.age <= int(m['age2']))
    except:
        pass
    try:
        p = p.filter(Post.destination.in_(m['destination']))
    except:
        pass

    try:
        p = p.filter(Post.color.in_(m['color']))
    except:
        pass
    try:
        if m['delivery']:
            p = p.filter(Post.delivery == 1)
    except:
        pass
    try:
        if m['price1']:
            if m['price2']:
                p = p.filter(int(m['price1']) <= Post.price <= int(m['price2']))
            else:
                p = p.filter(Post.price >= int(m['price1']))
        elif m['price2']:
            p = p.filter(Post.price <= int(m['price2']))
    except:
        pass
    try:
        if m['documents']:
            p = p.filter(Post.documents == 1)
    except:
        pass
    try:
        if m['vaccin']:
            p = p.filter(Post.vaccin == 1)
    except:
        pass
    try:
        if m['steril']:
            p = p.filter(Post.steril == 1)
    except:
        pass
    p = p.all()
    posts = list(
        map(lambda x: [x.title[:9] + '...' if len(x.title) > 9 else x.title, x.destination, x.price, x.currency,
                       x.address[:20] + '...' if len(x.address) > 20 else x.address, x.photo, x.id] if
        ll2 >= x.coords1 >= ll1 and ll4 >= x.coords2 >= ll3 else None, p))
    if len(city) > 70:
        city = city[:70] + '...'
    session['link2'] = f"/category/{types}/posts"
    if all(i == None for i in posts):
        posts = []
    return render_template('posts.html', title=str(types), posts=posts, city=city, back=f"/category/{types}")


@app.route('/category/<types>', methods=['GET', 'POST'])
def subcategory(types):
    f = open('category.json', encoding="utf8")
    r = json.load(f)
    sb = []
    if request.method == "POST":
        if 'назад' in request.values:
            return redirect(f'/category')
        for i in request.values:
            sb.append(i)
        session["categories"] = sb
        return redirect(f'/category/{types}/posts')
    if types in r:
        m = r[f"{types}"]['types']
        name = r[f"{types}"]['name']
        return render_template('subcategory.html', title=str(types), name=name, types=m)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    session["link2"] = '/profile'
    session["link1"] = '/profile'
    form = PhotoForm()
    if current_user.is_authenticated:
        if request.method == "POST":
            if form.photo.data:
                os.remove('/'.join(os.getcwd().split(
                    '\\')) + current_user.photo)
                file = Image.open(form.photo.data, mode='r', formats=None)
                if file:
                    w, h = file.size
                    if w > h:
                        file = file.crop((w - (w - h) // 2 - h, 0, w - (w - h) // 2, h))
                    if w < h:
                        file = file.crop((0, h - (h - w) // 2 - w, w, h - (h - w) // 2))
                    file.save(
                        '/'.join(os.getcwd().split(
                            '\\')) + f'/static/avatars/{current_user.id}/{form.photo.data.filename}')
                    ph = f'/static/avatars/{current_user.id}/{form.photo.data.filename}'
                    current_user.photo = ph
                    dbs = db_session.create_session()
                    dbs.merge(current_user)
                    dbs.commit()
                    return redirect('/profile')
            for i in request.values:
                if i.isdigit():
                    dbs = db_session.create_session()
                    del_p = dbs.query(Post).filter(Post.id == i).first()
                    shutil.rmtree('/'.join(os.getcwd().split(
                        '\\')) + f'/static/pets_photo/{str(i)}')
                    dbs.delete(del_p)
                    dbs.commit()
        if len(current_user.city) > 40:
            city = current_user.city[:40] + '...'
        else:
            city = current_user.city
        dbs = db_session.create_session()
        posts = dbs.query(Post).filter(Post.user == current_user).order_by(Post.created_date).all()
        posts = list(
            map(lambda x: [x.title[:9] + '...' if len(x.title) > 9 else x.title, x.price, x.currency, x.views_count,
                           x.photo, x.id, x.created_date.strftime('%d.%m.%Y, %H:%M')], posts))
        session['link'] = '/profile'
        return render_template('profile.html', title='Профиль', city=city, posts=posts, form=form)
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


@app.route('/about_site')
def about():
    return render_template('about_site.html', title='Информация о сайте')


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
                                   message="Почта уже используется")
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
        os.makedirs('/'.join(os.getcwd().split('\\')) + f'/static/avatars/{user.id}', exist_ok=True)
        file = Image.open('/'.join(os.getcwd().split('\\')) + '/static/img/avatar.png', mode='r', formats=None)
        file.save(
            '/'.join(os.getcwd().split('\\')) + f'/static/avatars/{user.id}/avatar.png')
        user.photo = f'/static/avatars/{user.id}/avatar.png'
        db_sess.commit()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/profile")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit():
    if current_user.is_authenticated:
        form = EditForm()
        if request.method == 'POST':
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(
                    User.email == form.email.data).first() and form.email.data != current_user.email:
                return render_template('change_profile.html', title='Редактирование',
                                       form=form,
                                       message="Почта телефона уже используется")
            s = db_sess.query(User).filter(User.id == current_user.id).first()
            s.name = form.name.data
            current_user.name = form.name.data
            s.email = form.email.data
            current_user.email = form.email.data
            s.about = form.about.data
            current_user.about = form.about.data
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect("/profile")
        else:
            form.email.data = current_user.email
            form.name.data = current_user.name
            form.about.data = current_user.about
        return render_template('change_profile.html', title='Редактирование', form=form)
    return redirect("/profile")


@app.route('/user/<uid>', methods=['GET', 'POST'])
def user(uid):
    db_sess = db_session.create_session()
    userr = db_sess.query(User).filter(User.id == uid).first()
    if userr == current_user:
        return redirect("/profile")
    posts = db_sess.query(Post).filter(Post.user_id == uid).all()
    posts = list(
        map(lambda x: [x.title, x.price, x.currency, x.address[:50] + '...' if len(x.address) > 50 else x.address,
                       x.photo, x.id, x.created_date.strftime('%d.%m.%Y, %H:%M'), x.destination,
                       x.content[:50] + '...' if len(x.content) > 50 else x.content], posts))
    return render_template('user.html', title=userr.name, userr=userr, posts=posts)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if current_user.is_authenticated:
        if request.method == "POST":
            if 'logout' in request.values:
                logout_user()
                return redirect("/profile")
            if 'del_acc' in request.values:
                ds = db_session.create_session()
                us = ds.query(User).filter(User.id == current_user.id).first()
                shutil.rmtree('/'.join(os.getcwd().split(
                    '\\')) + f'/static/avatars/{current_user.id}')
                ds.delete(us)
                ds.commit()
                logout_user()
                return redirect("/profile")
        return render_template('settings.html', title='Настройки')
    return redirect("/profile")


@app.route('/search', methods=['GET', 'POST'])
def search():
    dbs = db_session.create_session()
    m = []
    lst = []
    session['link'], session['link2'] = '/search', '/search'
    if request.method == 'POST':
        for i in request.values:
            m = request.values[i].split()
            m = list(map(lambda x: "".join(c for c in x if c.isalnum()), m))
            for j in m:
                if len(j) > 2:
                    j = j[:-1]
                posts = dbs.query(Post).filter((Post.content.like(f'%{j}%')) | (Post.title.in_(m)) | (
                    Post.content.like(f'%{j.lower()}%')) | (Post.content.like(f'%{j.capitalize()}%')) |
                                               (Post.content.like(f'%{j.upper()}%')) | (
                                                   Post.breed.like(f'%{j.capitalize()}%')) | (
                                                   Post.category.like(f'%{j.capitalize()}%')) | (
                                                   Post.breed.like(f'%{j.lower()}%'))).all()
                if posts:
                    for h in posts:
                        lst.append(h)
    lst = list(
        map(lambda x: [x.title, x.destination, x.price, x.currency, x.delivery,
                       x.content[:50] + '...' if len(x.content) > 50 else x.content,
                       x.address[:50] + '...' if len(x.address) > 50 else x.address,
                       x.created_date.strftime('%d.%m.%Y, %H:%M'), x.photo, x.id], lst))
    if lst:
        session['request_s'] = lst
    print(session['request_s'])
    return render_template('search_request.html', title='Поиск', lst=session['request_s'], ln=len(session['request_s']))


if __name__ == '__main__':
    db_session.global_init("db/pets.db")
    app.run(port=8080, host='127.0.0.1')
