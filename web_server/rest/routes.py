import flask

from my_log import LOG
from web_server.rest import controller, rest_utils

app = flask.Blueprint('my_api', __name__, url_prefix='/github')


@app.route('/projects/<path:project_name>')
@rest_utils.expected_errors(404)
def get_project(project_name: str):
    """ Get project details

    :param: project_name:
    :return:              Project details

    Example request:
        GET /github/projects/pallets/flask
    """
    data = controller.get_project(project_name)
    LOG.debug(f'get_project [{project_name}]: {data}')
    return data


@app.route('/packages/<path:package_name>')
@rest_utils.expected_errors(404)
def get_package(package_name: str):
    """ Set admin state

    :param: project_name:
    :return:              Project details

    Example request:
        GET /github/packages/mediapy
    """
    data = controller.get_package(package_name)
    LOG.debug(f'get_package [{package_name}]: {data}')
    return data


@app.route('/requests', methods=['POST'])
@rest_utils.normal_response(202)
@rest_utils.expected_errors(400)
def start_process():
    """ Create new request

    :return:

    Example request:
        POST /github/requests  {"num_of_projects": 5}
    """
    js = flask.request.json
    LOG.debug(f'start_process: {js}')
    controller.start_process(js)
    return ''
