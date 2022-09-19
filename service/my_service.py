import multiprocessing
import re
import time
import hashlib

from my_log import LOG
from my_utils.queue import MyQueue
from my_utils.settings import get_github_token
from objects.enum import RequestStatus, ProjectStatus
from objects.request import Request
from objects.project import Project
from objects.project_package import ProjectPackage
from service.github_api import process_request, process_project


class MyService:
    def __init__(self, max_processes: int = 20):
        self.max_processes = max_processes
        self.curr_processes = 0
        self.token = get_github_token()
        super().__init__()

    def _dec_curr_process(self):
        """
        Decreases the current process counter by one
        :return:
        """
        if 0 < self.curr_processes:
            self.curr_processes -= 1
        else:
            LOG.error(f'Cannot decrease curr_processes ({self.curr_processes})')

    def _run_process(self):
        """
        Tries to run process of request or projects details. Limit the nuber of subprocesses with max_processes
        :return:
        """
        if self.curr_processes < self.max_processes:
            # Look for requests in 'init' status:
            open_requests = Request.get_list({'status': RequestStatus.INIT})
            for request in open_requests:
                process = multiprocessing.Process(target=process_request, args=(self.token, request.id, request.length))
                process.start()
                request.status = RequestStatus.PROCESSING
                request.pid = process.pid
                request.update()

                self.curr_processes += 1
                LOG.info(f'New process was create successfully for request {request.id}')

                if self.max_processes <= self.curr_processes:
                    break

            # Look for projects without details:
            open_projects = Project.get_list({'status': ProjectStatus.INIT})
            for project in open_projects:
                process = multiprocessing.Process(target=process_project, args=(self.token, project.id, project.name))
                process.start()
                project.status = RequestStatus.PROCESSING
                project.pid = process.pid
                project.update()

                self.curr_processes += 1
                LOG.info(f'New process was create successfully for project {project.name}')

                if self.max_processes <= self.curr_processes:
                    break
            else:
                if self.curr_processes < self.max_processes:
                    # There's no work do!
                    LOG.debug('Yep! No more work to do!')

    @staticmethod
    def start_process(data: dict):
        """
        Add a new request to DB
        :param data: JSON with the number of project to request
        :return:
        """
        LOG.debug(f'start_process : {data}')
        length = data.get('num_of_projects')
        if length:
            request = Request(length)
            request.create()
        else:
            LOG.error(f'start_process: Invalid length ({length})')

    def project_list(self, data: dict):
        """
        Add the project list to DB.
        :param data: JSON with request index and list of project
        :return:
        """
        self._dec_curr_process()
        request_id = data.get('request_id')
        status = data.get('status')
        request = Request.get(id=request_id)
        if request:
            request.status = status
            request.update()
            LOG.info(f'Request {request_id} is {status}!')
        else:
            LOG.error(f'Request {request_id} was not found!')

        # Update project list:
        prj_list = data.get('project_list')
        for project_name in prj_list:
            project = Project.get(name=project_name)
            if not project:
                project = Project(project_name)
                project.create()
                LOG.info(f'New project {project_name} was add successfully!')
            else:
                LOG.debug(f'Project {project_name} already exist')

    def project_package_list(self, data: dict):
        """
        Add package list to a project
        :param data: information of the project and package list
        :return:
        """
        self._dec_curr_process()

        project_id = data.get('project_id')
        status = data.get('status')
        project = Project.get(id=project_id)
        if project:
            package_list = data.get('package_list')
            if package_list:
                # Calculate checksum:
                project.checksum = hashlib.md5(package_list.encode('utf-8')).hexdigest()

                # Update project-packages relationship:
                for package_name in package_list.split('\n'):
                    # Split between the package name and its version (if there is):
                    arr = re.findall(r'(^\w[\w-]*)(.*)', package_name.strip())
                    if arr and arr[0]:
                        name = arr[0][0]
                        version = arr[0][1]
                        package = ProjectPackage(project.id, name, version)
                        package.create()
                        LOG.info(f'New relationship : {project.name} => {name} ({version})')

            project.status = status
            project.update()
            LOG.info(f'Project {project.name} ({project_id}) is {status}!')
        else:
            LOG.error(f'Project {project_id} was not found!')

    def run(self):
        # Create listener
        MyQueue.listener()

        while True:
            try:
                # Try to run process:
                self._run_process()

                action, data = MyQueue.get()
                LOG.debug(f'Service: {action} : {data}')

                if hasattr(self, action):
                    func = getattr(self, action)
                    func(data)
                else:
                    LOG.error(f'Invalid action ({action})')
            except Exception as e:
                LOG.exception(f'MyService Run: {e}')
                time.sleep(2)
