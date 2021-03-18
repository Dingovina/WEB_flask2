import flask

from data import db_session
from data.jobs import Jobs
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
        job = db_sess.query(Jobs).filter(Jobs.id == form.id.data).first()
        if not job:
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
            return render_template('add_job.html', title='New Job', form=form, message='Id already exists')
    return render_template('add_job.html', title='New Job', form=form)


@blueprint.route('/api/jobs/<job_id>')
def get_job(job_id):
    db_sess = db_session.create_session()
    if job_id == 'all':
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {
                'jobs':
                    [item.to_dict(
                        only=('id', 'team_leader', 'job_title', 'work_size', 'collaborators', 'is_finished', 'user_id'))
                        for item in jobs]
            }
        )
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
                    'Invalid job id.'
            }
        )


@blueprint.route('/api/jobs/delete/<job_id>')
def delete(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
        return f'Job was deleted.'
    else:
        return 'Invalid job id.'


@blueprint.route('/api/jobs/correct/<job_id>', methods=["GET", "POST"])
def correct(job_id):
    db_sess = db_session.create_session()
    form = AddingJobForm()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        if form.validate_on_submit():
            a_job = db_sess.query(Jobs).filter(Jobs.id == form.id.data).first()
            if a_job == job or not a_job:
                job.id = form.id.data
                job.job_title = form.job_title.data
                job.team_leader = form.team_leader_id.data
                job.work_size = form.work_size.data
                job.collaborators = form.collaborators.data
                job.is_finished = form.is_finished.data
                db_sess.add(job)
                db_sess.commit()
                return 'Форма отправлена'
        return render_template('add_job.html', title='New Job', form=form, to_cor=job)
    else:
        return 'Invalid job id.'


@blueprint.route('/api/jobs/correct/<job_id>/<new_id>/<new_title>/<new_leader>/<new_size>/<new_coll>/<new_finished>',
                 methods=["GET", "POST"])
def auto_correct(job_id, new_id="", new_title="", new_leader="", new_size="", new_coll="", new_finished=""):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        if all([new_id, new_title, new_leader, new_size, new_finished]):
            a_job = db_sess.query(Jobs).filter(Jobs.id == new_id).first()
            if a_job == job or not a_job:
                if new_finished not in ['True', 'False']:
                    return 'Parameter \"is_finished\" is not boolean.'
                else:
                    job.id = new_id
                    job.job_title = new_title
                    job.team_leader = new_leader
                    job.work_size = new_size
                    job.collaborators = new_coll
                    job.is_finished = bool(new_finished)
                    db_sess.commit()
                    return 'Форма отправлена.'
            else:
                return 'Id already exist.'
        else:
            return 'Not all parameters are indicated.'
    else:
        return 'Invalid job id.'
