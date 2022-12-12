import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import db
from user import User

import json


#app config
DEBUG = True
SECRET_KEY = os.environ.get('secret_key')
app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager(app)

# what to say and to where redirect when unauth person trying to visit somethig special
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(phone):
    return User().init_by_phone(phone)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('myself'))
    return render_template('start.html')


@app.route("/signin", methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('myself.html'))

    if request.method == 'POST':
        phone = request.form['phone']
        user_dict = db.get_user_by_phone(phone)
        remember = True if request.form.get('remainme') else False
        if user_dict and check_password_hash(user_dict['password'], request.form['password']):
            login_user(User().init_by_dict(user_dict), remember=remember)
            return redirect(request.args.get('next') or url_for('myself'))
        else:
            flash('Неверный логин, пароль', 'error')
    return render_template('signin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        if len(request.form['phone']) > 0 and len(request.form['psw']) > 0:
            hash = generate_password_hash(request.form['psw'])
            db.add_user(request.form['name'],
            request.form['surname'],
            request.form['fname'],
            request.form['passport'],
            request.form['country'],
            request.form['phone'],
            hash)
            return redirect(url_for('signin'))
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("signup.html")


@app.route('/myself')
@login_required
def myself():
    return render_template("myself.html")

@app.route('/ensure_car')
@login_required
def ensure_car():
    types = db.get_car_types()
    return render_template("ensure_car.html", types=types)

@app.route('/ensure_life')
@login_required
def ensure_life():
    types = db.get_life_types()
    return render_template("ensure_life.html", types=types)

@app.route('/ensure_car/<id>', methods=["POST", "GET"])
@login_required
def ensure_car_n(id):
    if request.method == "POST":
        db.add_car(
            request.form['vin'],
            request.form['number'],
            request.form['mark'],
            request.form['model'],
            request.form['year'],
        )
        car_id = db.get_car_id(request.form['vin'])['id']
        db.add_car_en(current_user.get_user()['id'], id, car_id)
        return render_template('confirm.html', item=db.get_ens_car(id), car_mark=request.form['mark'], car_num=request.form['number'])
    return render_template("selectcar.html", id=id)

@app.route('/ensure_life/<id>')
@login_required
def ensure_life_n(id):
    db.add_life_en(current_user.get_user()['id'], id)
    return render_template('confirm.html', item=db.get_ens_life(id), car_mark=None)

@app.route('/my_ensurs')
@login_required
def my_ens():
    return render_template('my_ens.html', car = db.get_my_cars(current_user.get_user()['id']), life =db.get_my_life(current_user.get_user()['id']))



if __name__ == "__main__":
    app.run(debug=True)
