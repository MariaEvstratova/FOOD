# from flask import jsonify
#
# from . import db_session
# from .jobs import Jobs
# from flask_restful import reqparse, abort, Api, Resource
#
#
# def abort_if_user_not_found(job_id):
#     session = db_session.create_session()
#     jobs = session.query(Jobs).get(job_id)
#     if not jobs:
#         abort(404, message=f"Job {job_id} not found")
#
#
# class JobsResource(Resource):
#     def get(self, job_id):
#         abort_if_user_not_found(job_id)
#         session = db_session.create_session()
#         job = session.query(Jobs).get(job_id)
#         return jsonify({'job': job.to_dict(
#             only=('team_leader', 'job', 'work_size', 'collaborators'))})
#
#     def delete(self, job_id):
#         abort_if_user_not_found(job_id)
#         session = db_session.create_session()
#         job = session.query(Jobs).get(job_id)
#         session.delete(job)
#         session.commit()
#         return jsonify({'success': 'OK'})
#
# class JobsListResource(Resource):
#     def get(self):
#         session = db_session.create_session()
#         jobs = session.query(Jobs).all()
#         return jsonify({'jobs': [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators')) for item in jobs]})
#
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('team_leader', required=True, type=int)
#         parser.add_argument('job', required=True, type=str)
#         parser.add_argument('work_size', required=True, type=int)
#         parser.add_argument('collaborators', required=True, type=str)
#
#         args = parser.parse_args()
#         session = db_session.create_session()
#         jobs = Jobs(
#             team_leader=args['team_leader'],
#             job=args['job'],
#             work_size=args['work_size'],
#             collaborators=args['collaborators']
#         )
#         session.add(jobs)
#         session.commit()
#         return jsonify({'success': 'OK'})