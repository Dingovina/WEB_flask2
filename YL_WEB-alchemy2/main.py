from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime
from flask import Flask, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class RegFrom(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    username = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddingJobForm(FlaskForm):
    job_title = StringField('Job title', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    data = []
    for job in jobs:
        save = {}
        lead = db_sess.query(User).filter(User.id == job.team_leader).first()
        coll = job.collaborators.split(', ')
        users = []
        for id in coll:
            coller = db_sess.query(User).filter(User.id == id).first()
            users.append(coller.name)
        save['id'] = job.id
        save['team_leader'] = lead.name
        save['job_title'] = job.job_title
        save['work_size'] = job.work_size
        save['colls'] = users
        save['is_finished'] = job.is_finished
        data.append(save)
    return render_template('index.html', data=data)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegFrom()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = User()
        if form.password.data == form.repeat_password.data:
            user.email = form.email.data
            user.password = form.password.data
            user.name = form.username.data
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('registration.html',
                               message="пароли не совпадают",
                               form=form)
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = AddingJobForm()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        if form.validate_on_submit():
            job = Jobs()
            job.job_title = form.job_title.data
            job.team_leader = current_user.id
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.add(job)
            db_sess.commit()
            return redirect('/')
    return render_template('addjob.html', form=form)


@app.route('/delete/<id>')
def delete_job(id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
        return redirect('/')
    else:
        return 'Invalid job id.'


@app.route('/correct/<id>', methods=["GET", "POST"])
def correct_job(id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        form = AddingJobForm()
        if form.validate_on_submit():
            job.job_title = form.job_title.data
            job.team_leader = current_user.id
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.add(job)
            db_sess.commit()
            return redirect('/')
        return render_template('addjob.html', form=form, job=job)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
