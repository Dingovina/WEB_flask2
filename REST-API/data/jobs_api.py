import flask

from . import db_session
from .jobs import Jobs
from flask import jsonify, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddingJobForm(FlaskForm):
    id = IntegerField('Job Id', validators=[DataRequired()])
    job_title = StringField('Job title', validators=[DataRequired()])
    team_leader_id = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/', methods=['GET', 'POST'])
@blueprint.route('/api/jobs', methods=['GET', 'POST'])
def get_jobs():
    form = AddingJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.id = form.id.data
        job.job_title = form.job_title.data
        job.team_leader = form.team_leader_id.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return 'Форма отправлена'
    else:
        render_template('add_job.html', title='New Job', form=form, message='Поля заполнены некорректно')
    return render_template('add_job.html', title='New Job', form=form)


@blueprint.route('/api/jobs/<job_id>')
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        return jsonify(
            {
                'jobs':
                    [job.to_dict(
                        only=(
                            'id', 'team_leader', 'job_title', 'work_size', 'collaborators', 'is_finished', 'user_id'))]
            }
        )
    else:
        return jsonify(
            {
                'response':
                    'Введён неверный параметр'
            }
        )
