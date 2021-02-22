from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    asrt_id = StringField('Id астронавта', validators=[DataRequired()])
    asrt_pass = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_id = StringField('Id капитана', validators=[DataRequired()])
    cap_pass = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    params = {'title': title}
    return render_template('base.html', **params)


@app.route('/training/<prof>')
def training(prof):
    params = {'prof': prof, 'title': 'training'}
    return render_template('training.html', **params)


@app.route('/list_prof/<type>')
def list_prof(type):
    list = ["инженер-исследователь", "пилот", "врач", "строитель", "эколог", "экзобиолог", "кламатолог",
            "инженер по терраформированию", "геолог", "астрогеолог", "метеоролог", "специалист по радиационной защите"]
    params = {'list': list, 'type': type, 'title': 'training'}
    return render_template('list_prof.html', **params)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    title = 'Answer'
    Surname = 'Иванов'
    Name = 'Иван'
    ed = 'приемлимое'
    prof = 'полезная'
    sex = 'male'
    motiv = '-'
    ready = True
    params = {'title': title, 'surname': Surname, 'name': Name, 'education': ed, 'profession': prof, 'sex': sex,
              'motivation': motiv, 'ready': ready}
    return render_template('auto_answer.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/distribution')
def distribution():
    data = ['Ридли Скотт', 'Энди Уир', 'Марк Уир', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    title = 'По каютам!'
    params = {'data': data, 'title': title}
    return render_template('distribution.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
