from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from data import db_session, jobs_api
from data.users import User
from data.food import Food
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.logf import LoginForm
from forms.user import RegisterForm
from forms.food import FoodForm
from data import users_resource, jobs_resource
from flask_restful import reqparse, abort, Api


def main():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    db_session.global_init("db/blogs1.db")
    # api = Api(app)
    # api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    # api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    # api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    # api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    # app.run()
    # db_sess = db_session.create_session()
    # user = User()
    # user.name = 'Евстратова Мария'
    # user.email = 'evstratova.mashenka@gmail.com'
    # user.hashed_password = 'mars'
    # user.role = 'admin'
    # db_sess.add(user)
    # db_sess.commit()
    # db_sess = db_session.create_session()
    # food = Food()
    # food.type = 'салат'
    # food.name = 'Оливье'
    # food.about = 'Помидоры, масло оливковое, сыр фета, орегано, маслины чёрные без косточек, перец болгарский, маслины, огурцы свежие'
    # food.price = '600 р'
    # food.image = 'greek.jpeg'
    # db_sess.add(food)
    # db_sess.commit()
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
        userr = db_sess.query(User).all()
        food = db_sess.query(Food).all()
        if current_user.is_authenticated:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.basket += ' ' + str(id)
            db_sess.commit()
            ids = user.basket.split()
            ids = [int(i) for i in ids]
            ids = ids[::-1]
            return render_template("basket_id.html", ids=ids, food=food, user=userr, id=id)
        return render_template("basket_id.html", message='', food=food, user=userr, id=id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
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
                return render_template ('register.html', title='Регистрация',
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
        db_sess = db_session.create_session()
        food = db_sess.query(Food).all()
        userr = db_sess.query(User).all()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        ids = user.basket.split()
        ids = [int(i) for i in ids]
        ids = ids[::-1]
        return render_template("basket.html", ids=ids, food=food, user=userr)
    #
    # @app.route('/jobs/<int:id>', methods=['GET', 'POST'])
    # @login_required
    # def edit_jobs(id):
    #     form = JobsForm()
    #     if request.method == "GET":
    #         db_sess = db_session.create_session()
    #         userr = 0
    #         for i in db_sess.query(User).filter(User.id == 1):
    #             userr = i
    #         jobs = db_sess.query(Jobs).filter((Jobs.id == id), ((Jobs.user == userr) |
    #                                                             (Jobs.user == current_user))
    #                                           ).first()
    #         if jobs:
    #             form.title.data = jobs.job
    #             form.team_leader.data = jobs.team_leader
    #             k = jobs.work_size
    #             form.work_size.data = str(k)
    #             form.collaborators.data = jobs.collaborators
    #             form.is_finished.data = jobs.is_finished
    #         else:
    #             abort(404)
    #     if form.validate_on_submit():
    #         db_sess = db_session.create_session()
    #         userr = 0
    #         for i in db_sess.query(User).filter(User.id == 1):
    #             userr = i
    #         jobs = db_sess.query(Jobs).filter((Jobs.id == id), ((Jobs.user == userr) |
    #                                                             (Jobs.user == current_user))
    #                                           ).first()
    #         if jobs:
    #             jobs.job = form.title.data
    #             jobs.team_leader = form.team_leader.data
    #             k = form.work_size.data
    #             jobs.work_size = int(k)
    #             jobs.collaborators = form.collaborators.data
    #             jobs.is_finished = form.is_finished.data
    #             db_sess.commit()
    #             return redirect('/')
    #         else:
    #             abort(404)
    #     return render_template('jobs.html',
    #                            title='Edit job',
    #                            form=form
    #                            )
    #
    # @app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
    # @login_required
    # def jobs_delete(id):
    #     db_sess = db_session.create_session()
    #     userr = 0
    #     for i in db_sess.query(User).filter(User.id == 1):
    #         userr = i
    #     jobs = db_sess.query(Jobs).filter((Jobs.id == id), ((Jobs.user == userr) |
    #                                       (Jobs.user == current_user))
    #                                       ).first()
    #     if jobs:
    #         db_sess.delete(jobs)
    #         db_sess.commit()
    #     else:
    #         abort(404)
    #     return redirect('/')

    # @app.errorhandler(404)
    # def not_found(error):
    #     return make_response(jsonify({'error': 'Not found'}), 404)
    #
    # @app.errorhandler(400)
    # def bad_request(_):
    #     return make_response(jsonify({'error': 'Bad Request'}), 400)

    app.run(port=8000, host='127.0.0.1')

if __name__ == '__main__':
    main()