from my_log import LOG
from my_utils.queue import MyQueue
from objects.enum import RequestStatus, ProjectStatus
from service.githubAPI2 import GithubClient, GithubRepo


def process_request(token: str, idx: int, length: int):
    """
    Gets a list of <length> projects written in Python
    :param token: GitHub token
    :param idx: index of the request in DB
    :param length: number of projects to request
    :return:
    """
    try:
        github_client = GithubClient(token=token)
        prj_list = github_client.get_popular_repos(number=length, language="Python")
        status = RequestStatus.READY
    except Exception as e:
        LOG.error(f'process_request [{idx}] : {e}')
        prj_list = []
        status = RequestStatus.ERROR

    # Prepare the update message to the service:
    data = {
        'request_id': idx,
        'status': status,
        'project_list': prj_list
    }
    MyQueue.send('project_list', data)


def process_project(token: str, idx: int, name: str):
    """
    Gets the package in use by the given project
    :param token: GitHub token
    :param idx: index of the project in DB
    :param name: Name of the project
    :return:
    """
    try:
        github_client = GithubClient(token=token)
        url = github_client.fetch_repo_archive_url(name)
        repo = GithubRepo(archive_url=url, token=token)
        package_list = repo.get_python_req_file_single_api()
        status = ProjectStatus.READY
    except Exception as e:
        LOG.exception(f'process_project [{name}] : {e}')
        package_list = ''
        status = ProjectStatus.ERROR

    # Prepare the update message to the service:
    data = {
        'project_id': idx,
        'status': status,
        'package_list': package_list
    }
    MyQueue.send('project_package_list', data)
