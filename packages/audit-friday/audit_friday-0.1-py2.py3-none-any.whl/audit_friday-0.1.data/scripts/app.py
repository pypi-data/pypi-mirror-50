from flask import Flask, request, jsonify
from datetime import timedelta
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity, verify_jwt_in_request, set_access_cookies
)
from scripts.core.handlers.login_handler import LoginHandler
# from gunicorn.app.base import Application, Config
# import gunicorn
# from gunicorn import glogging
# from gunicorn.workers import sync
from gunicorn.six import iteritems
import multiprocessing
from scripts.constants import app_configuration, app_constants
from scripts.services import model_repo_services
from scripts.services import projects_services
from scripts.services import dataset_services
from scripts.services import model_list_services
from scripts.services import data_pipeline_services
from scripts.services import project_list_services
from scripts.services import jobs_services
from scripts.services import airflow_plugin_service
from scripts.services import login_services
from scripts.services import dashboard_services
from scripts.services import settings_services
from scripts.services import component_services
from scripts.services import download_service
from scripts.services import project_activity_services
from scripts.services import s3_services
from scripts.services import kubernetes_services
from scripts.services import notification_service
from scripts.services import search_service
from scripts.services import alerts_service
from scripts.services import data_catalog_service
from scripts.services import rstudio_services
from scripts.services import billing_services
from scripts.services import workbench_services
from scripts.services import registry_services
from scripts.services import kubernetes_client_services
from scripts.services import container_deployment_services
from scripts.services import pipeline_api_services
from scripts.services import streaming_services


# -----------------------------------------CORS configurations for Service Endpoints------------------------------------

app = Flask(__name__)
app.secret_key = app_constants.Encryption.ENCRYPTION_KEY
app.config['JWT_TOKEN_LOCATION'] = 'cookies'
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=app_configuration.SESSION_TIMEOUT_IN_MINUTES)
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)
app.register_blueprint(model_repo_services.model_repo)
app.register_blueprint(projects_services.projects)
app.register_blueprint(project_list_services.project_list)
app.register_blueprint(dataset_services.dataset)
app.register_blueprint(model_list_services.model_list)
app.register_blueprint(data_pipeline_services.data_pipeline)
app.register_blueprint(jobs_services.jobs)
app.register_blueprint(airflow_plugin_service.air_flow)
app.register_blueprint(login_services.login)
app.register_blueprint(dashboard_services.dashboard)
app.register_blueprint(settings_services.settings)
app.register_blueprint(component_services.component)
app.register_blueprint(download_service.download_component)
app.register_blueprint(project_activity_services.projects_activity)
app.register_blueprint(s3_services.s3Browser)
app.register_blueprint(kubernetes_services.kubernetes)
app.register_blueprint(notification_service.notifications)
app.register_blueprint(search_service.search)
app.register_blueprint(alerts_service.alert)
app.register_blueprint(data_catalog_service.data_catalog)
app.register_blueprint(rstudio_services.rstudio)
app.register_blueprint(billing_services.billing)
app.register_blueprint(workbench_services.workbench)
app.register_blueprint(registry_services.registry)
app.register_blueprint(container_deployment_services.container_deployment)
app.register_blueprint(kubernetes_client_services.kubernetes_client)
app.register_blueprint(pipeline_api_services.pipeline_api)
app.register_blueprint(streaming_services.streaming)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# todo:Remove add_job_status endpoint from session_validate before request

# @app.before_request
# def session_validate_before_request():
#     """
#     This is a method to validate the session before every service call
#     :return:
#     """
#     if app_configuration.APPLY_SESSION:
#         if request.endpoint not in ['login.verify_login', 'pipeline_api.enable_api', 'pipeline_api.trigger_pipeline_from_api', 'pipeline_api.get_job_status', 'pipeline_api.disable_api']:
#             verify_jwt_in_request()
#
#
# @app.after_request
# def update_session_after_login(response):
#     """
#     This is a method to update the session token after the request
#     :param response: The response from the services
#     :return:
#     """
#     if app_configuration.APPLY_SESSION:
#         if request.endpoint not in ['login.session_logout', 'notifications.get_notifications']:
#             current_user = get_jwt_identity()
#             if current_user is not None:
#                 access_token = create_access_token(identity=current_user)
#                 set_access_cookies(response, access_token)
#                 return response
#         return response
#
#
# # Using the expired_token_loader decorator, we will now call
# # this function whenever an expired but otherwise valid access
# # token attempts to access an endpoint
# @jwt.expired_token_loader
# def custom_message_after_session_token_expired():
#     user_id = request.headers.get(app_constants.CommonConstants.REQUEST_HEADER_USER)
#     session_obj = LoginHandler()
#     session_obj.capture_session_logout(user_id)
#     return jsonify({
#         'status': 401,
#         'message': 'un-authorized'
#     }), 401


# ---------------------------------------------------------------------------------------------------------------------

@app.route(app_configuration.api_service_url + '/version', methods=["GET"])
def route():
    if request.method == 'GET':
        return "------------------ AI Lens UI Services ---- version: " \
               "{version} ------------------".format(version=app_configuration.VERSION)
    else:
        return "Method Not supported!"


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(app_configuration.PORT), debug=True, threaded=True, use_reloader=False)


def number_of_workers():
    """
    Finds the number of workers based on cpu count.
    :return: number_of_workers: number of workers
    :return: (multiprocessing.cpu_count()) + 1
    """
    try:
        apply_processor_count = app_configuration.APPLY_PROCESSOR_COUNT
        if apply_processor_count:
            return (multiprocessing.cpu_count()) + 1
        else:
            return int(app_configuration.WORKERS)
    except Exception as ex:
        print('error in getting workers count :' + str(ex))
        return 1


# class GunicornFlaskApplication(Application):
#     def __init__(self, application, option):
#         """
#         Initializing the class variables required for running application.
#         :param app: flask application object
#         :param options: json containing number of workers, host and port information
#         """
#         self.usage, self.callable, self.prog, self.app = None, None, None, application
#         self.option = option
#
#     def run(self, **option):
#         """
#         Runs the application on gunicorn server.
#         :param option:
#         :return:
#         """
#         self.cfg = Config()
#         config = dict([(key, value) for key, value in iteritems(self.option)
#                        if key in self.cfg.settings and value is not None])
#         for key, value in iteritems(config):
#             self.cfg.set(key.lower(), value)
#         return Application.run(self)
#     load = lambda self:self.app

# if __name__ == "__main__":
#     options = {
#         'bind': '%s:%s' % ("0.0.0.0", app_configuration.PORT),
#         'workers': number_of_workers(),
#     }
#     gunicorn_app = GunicornFlaskApplication(app, options)
#     gunicorn_app.run(
#         worker_class="gunicorn.workers.sync.SyncWorker",
#     )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(app_configuration.PORT), debug=True, threaded=True, use_reloader=False)
