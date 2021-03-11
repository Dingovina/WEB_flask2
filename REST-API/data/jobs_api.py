import flask

from . import db_session
from .jobs import Jobs
from flask import jsonify

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/')
@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(
                    only=('id', 'team_leader', 'job_title', 'work_size', 'collaborators', 'is_finished', 'user_id'))
                    for item in jobs]
        }
    )


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
