from app import db
from objects.enum import RequestStatus
from objects.base_obj import BaseObj


class Request(BaseObj, db.Model):
    __tablename__ = 'requests'
    name = db.Column('name', db.String(BaseObj.NAME_SIZE), nullable=True)
    length = db.Column('length', db.Integer, default=0)
    status = db.Column('status', db.String(48), default=RequestStatus.INIT)
    pid = db.Column('pid', db.Integer, default=0)

    def __init__(self, length: int):
        self.name = f'request {self.id}'
        self.length = length
        super().__init__()
