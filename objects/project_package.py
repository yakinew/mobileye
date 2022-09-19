from app import db
from objects.base_obj import BaseObj


class ProjectPackage(BaseObj, db.Model):
    __tablename__ = 'project_packages'
    project_id = db.Column('project_id', db.String(48), nullable=False)
    name = db.Column('name', db.String(BaseObj.NAME_SIZE), nullable=True)
    version = db.Column('version', db.Text, default='')

    def __init__(self, project_id: int, package_name: str, version: str = ''):
        self.project_id = project_id
        self.name = package_name
        self.version = version
        super().__init__()
