from app import db
from objects.enum import ProjectStatus
from objects.base_obj import BaseObj


class Project(BaseObj, db.Model):
    __tablename__ = 'projects'
    status = db.Column('status', db.String(48), default=ProjectStatus.INIT)
    pid = db.Column('pid', db.Integer, default=0)
    checksum = db.Column('checksum', db.Text, default='')

    def __init__(self, project_name: str):
        self.name = project_name
        super().__init__()

    @property
    def package_list(self):
        # Look for packages only if project record is ready:
        if self.status == ProjectStatus.READY:
            from objects.project_package import ProjectPackage

            pp = ProjectPackage.get_list({'project_id': self.id})
            package_list = [p.name for p in pp]
        else:
            package_list = None
        return package_list

    def get_details(self):
        js = super().get_details()
        js['package_list'] = self.package_list
        del (js['pid'])
        return js
