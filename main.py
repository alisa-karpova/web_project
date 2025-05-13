from flask import Flask, render_template, redirect, abort, request, make_response, jsonify
from flask_login import login_required, logout_user, login_user, current_user, LoginManager

from project.data import db_session, snbs_api
from project.data.snowboards import Snowboards
from project.data.users import User
from project.forms.snowboard import SnowboardsForm
from project.forms.user import RegisterForm, LoginForm

from snb_search import check, find_snowboard

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

levels = {
    "beginner": "Начинающий (не освоил базовую технику)",
    "experienced": "Имею опыт катания (освоил базовую технику)",
    "pro": "Профи"
}
styles = {"base": "Базовая техника",
          "carving": "Карвинг",
          "freestyle": "Фристайл",
          "freeride": "Фрирайд",
          "carving_freestyle": "Карвинг и фристайл",
          "carving_freeride": "Карвинг и фрирайд"
          }


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/", defaults={'param': 'all'})
@app.route("/<param>")
def index(param):
    db_session.global_init("db/snb.db")
    db_sess = db_session.create_session()

    if current_user.is_authenticated:
        dic = {}
        if param == 'high':
            snbs = db_sess.query(Snowboards).filter(Snowboards.owner == current_user.id,
                                                    Snowboards.high_tramps == True)
        elif param == 'not_high':
            snbs = db_sess.query(Snowboards).filter(Snowboards.owner == current_user.id,
                                                    Snowboards.high_tramps == False)
        else:
            snbs = db_sess.query(Snowboards).filter(Snowboards.owner == current_user.id)

        if snbs:
            for snb in snbs:
                user = db_sess.query(User).filter(User.id == snb.owner).first()
                dic[snb.owner] = user.name

                return render_template("index.html", title='Сноуборды', snbs=snbs, dic=dic, user=user)

        return render_template("index.html", title='Сноуборды', snbs=snbs, dic=dic, user=current_user)

    else:
        return render_template("main_page.html")


@app.route("/navi")
@login_required
def navi():
    return render_template("main_page.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
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
                                   message="Такой пользователь уже существует")
        user = User(
            email=form.email.data,
            name=form.name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


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
                               message="Неверный пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/snbs',  methods=['GET', 'POST'])
@login_required
def add_snb():
    global levels, styles
    form = SnowboardsForm()

    if form.validate_on_submit():
        snb = Snowboards()
        message = check(form)
        if message == 'Все данные заполнены корректно':
            db_sess = db_session.create_session()
            res = find_snowboard(form)

            snb.owner_id = current_user.id
            snb.owner_weight = form.weight.data
            snb.owner_height = form.height.data
            snb.owner_level = levels[form.level.data]
            snb.owner_style = styles[form.style.data]

            snb.stiffness = res[0]
            snb.shape = res[1]
            snb.deflection = res[2]
            snb.height = res[3]
            snb.high_tramps = form.high_tramps.data

            current_user.snbs.append(snb)
            db_sess.merge(current_user)
            db_sess.commit()

            return redirect('/')
        else:
            return render_template('snowboards.html', title='Новый сноуборд',
                                   form=form, message=message)

    return render_template('snowboards.html', title='Новый сноуборд',
                           form=form)


@app.route('/snbs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_snb(id):
    global levels, styles
    form = SnowboardsForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        snb = db_sess.query(Snowboards).filter(Snowboards.id == id,
                                               Snowboards.owner == current_user.id).first()
        if snb:
            return render_template('snowboards.html',
                                   title='Изменение сноуборда',
                                   form=form)
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        message = check(form)
        snb = db_sess.query(Snowboards).filter(Snowboards.id == id,
                                               Snowboards.owner == current_user.id
                                              ).first()
        if snb:
            if message == 'Все данные заполнены корректно':
                res = find_snowboard(form)

                snb.owner_id = current_user.id
                snb.owner_weight = form.weight.data
                snb.owner_height = form.height.data
                snb.owner_style = styles[form.style.data]
                snb.owner_level = levels[form.level.data]

                snb.stiffness = res[0]
                snb.shape = res[1]
                snb.deflection = res[2]
                snb.height = res[3]
                snb.high_tramps = form.high_tramps.data

                db_sess.commit()
                return redirect('/')
            else:
                return render_template('snowboards.html',
                                       title='Изменение сноуборда',
                                       form=form, message=message
                                       )

    return render_template('snowboards.html',
                           title='Изменение сноуборда',
                           form=form
                           )


@app.route('/snbs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def snb_delete(id):
    db_sess = db_session.create_session()
    snb = db_sess.query(Snowboards).filter(Snowboards.id == id,
                                           Snowboards.owner == current_user.id
                                           ).first()
    if snb:
        db_sess.delete(snb)
        db_sess.commit()
    else:
        abort(404)

    return redirect('/')


def main():
    db_session.global_init("db/snb.db")
    app.register_blueprint(snbs_api.blueprint)


if __name__ == '__main__':
    main()
    app.run(port=8000, host='127.0.0.1')