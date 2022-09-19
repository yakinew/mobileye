import my_exception
from my_log import LOG
from my_utils.queue import MyQueue
from objects.project import Project
from objects.project_package import ProjectPackage


def get_project(project_name: str):
    # Check if project exists:
    project = Project.get(name=project_name)
    if not project:
        LOG.error(f'Project {project_name} could not be found!')
        raise my_exception.ProjectNotFound(project_name=project_name)

    data = project.get_details()
    return data


def get_package(package_name: str):
    # Check if project exists:
    project_packages = ProjectPackage.query.\
        join(Project, ProjectPackage.project_id == Project.id)\
        .add_columns(Project.name)\
        .filter(ProjectPackage.name == package_name).all()

    if not project_packages:
        LOG.error(f'Package {package_name} could not be found!')
        raise my_exception.PackageNotFound(package_name=package_name)

    project_list = [project[1] for project in project_packages]
    data = {
        'name': package_name,
        'projects': project_list
    }

    return data


def start_process(js: dict):
    # Validate input:
    if 'num_of_projects' not in js:
        LOG.error(f'Required parameter "num_of_projects" is missing!')
        raise my_exception.InvalidJsonScheme(scheme_error='Required parameter \'num_of_projects\' is missing!')

    # Send request to background service
    MyQueue.send('start_process', js)
