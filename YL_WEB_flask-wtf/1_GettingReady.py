from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
