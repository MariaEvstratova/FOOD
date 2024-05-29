from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from data import db_session, jobs_api
from data.users import User
from data.food import Food
from data.baskets import Basket
import os
from data.purchase import Purchase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.logf import LoginForm
from forms.user import RegisterForm
from forms.food import FoodForm
from forms.basket import BasketForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs1.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
def index():
    form = FoodForm()
    id = 1
    db_sess = db_session.create_session()
    userr = db_sess.query(User).all()
    food = db_sess.query(Food).all()
    return render_template("index.html", food=food, user=userr, form=form, id=id)


@app.route("/food/<int:id>")
def food(id):
    db_sess = db_session.create_session()
    userr = db_sess.query(User).all()
    food = db_sess.query(Food).filter(Food.id == id).first()
    return render_template("buy.html", food=food, user=userr, id=id)


@app.route("/basket/<int:id>")
def basket_id(id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.basket += ' ' + str(id)
        baskett = Basket()
        baskett.id_product = id
        baskett.id_user = user.id
        db_sess.add(baskett)
        db_sess.commit()
        return redirect('/basket')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.basket = ' '
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/basket')
def basket():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        food = db_sess.query(Food).all()
        userr = db_sess.query(User).all()
        basket = db_sess.query(Basket).all()
        baskets = []
        price = 0
        for i in basket:
            if i.id_user == current_user.id:
                baskets.append(i)
        if baskets == []:
            baskets = 'Nothing'
        else:
            for j in baskets:
                id_of_product = j.id_product
                for i in food:
                    if i.id == id_of_product:
                        price += int(i.price.split()[0])
            baskets = baskets[::-1]
        return render_template("basket.html", baskets=baskets, food=food, user=userr, price=price)
    return render_template("basket.html")

@app.route('/buying', methods=['GET', 'POST'])
def buying():
    form = FoodForm()
    db_sess = db_session.create_session()
    basket = db_sess.query(Basket).all()
    baskets = []
    for i in basket:
        if i.id_user == current_user.id:
            baskets.append(i)
    price = 0
    names = []
    for i in baskets:
        good = db_sess.query(Food).filter(Food.id == i.id_product).first()
        names.append(good.name)
    names = ', '.join(names)
    for i in baskets:
        food = db_sess.query(Food).filter(Food.id == i.id_product).first()
        price += int(food.price.split()[0])
    if request.method == "GET":
        return render_template('buying.html', form=form, price=price)
    else:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            buying = Purchase()
            buying.name = str(form.name.data)
            buying.number = str(form.number.data)
            buying.purchase = names
            buying.price = str(price)
            buying.id_buyer = int(user.id)
            buying.address = form.address.data
            db_sess.add(buying)
            db_sess.commit()
            items = db_sess.query(Basket).filter(Basket.id_user == current_user.id)
            for item in items:
                db_sess.delete(item)
                db_sess.commit()
            return redirect('/purchases')
        else:
            mess = "Error"
            return render_template('buying.html', form=form, price=price, message=mess)

@app.route('/purchases')
def purchases():
    db_sess = db_session.create_session()
    purchase = db_sess.query(Purchase).all()
    userr = db_sess.query(User).all()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    purch = {}
    for i in purchase:
        if i.id_buyer == user.id:
            if i.created_date not in purch:
                purch[i.created_date] = [i]
            else:
                purch[i.created_date].append(i)
                purch[i.created_date] = purch[i.created_date][::-1]
    if len(purch) == 0:
        return render_template("purchases.html", purch=purch, purchases=purchase, user=userr,
                                   message='Пока никаких покупок не совершено')
    purch = dict(sorted(purch.items()))
    print(purch)
    return render_template("purchases.html", purch=purch, purchases=purchase, user=userr, message=' ')

@app.route('/delete_item/<int:id>')
def delete_item(id):
    db_sess = db_session.create_session()
    item = db_sess.query(Basket).filter(Basket.id == id).first()
    if item:
        db_sess.delete(item)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/basket')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
