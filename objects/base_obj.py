import datetime
import my_exception
from app import db
from my_log import LOG


class BaseObj:
    """
    Basic class for object
    """
    NAME_SIZE = 64
    now = datetime.datetime.now

    id = db.Column('ID', db.Integer, primary_key=True)
    name = db.Column('name', db.String(NAME_SIZE), unique=True, nullable=False)
    created_at = db.Column('created_at', db.DateTime, default=now)

    def __init__(self):
        self.create_db()

    @staticmethod
    def date_format(dt):
        """
        Convert date and time to Openstack format (2015-11-29T22:21:42Z)
        :return: Random UUID
        """
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def create_db():
        """ Creates all tables """
        try:
            db.create_all()
            db.session.commit()
        except Exception as e:
            LOG.exception(f'Failed to create database : {e}')
            print(f'Failed to create database : {e}')

    @classmethod
    def table_exist(cls):
        """Check if the table """
        return db.engine.has_table(cls.__tablename__)

    @classmethod
    def _set_filter(cls, filter_list: list, key: str, value: str):
        if type(value) == str:
            if value.startswith('gt:'):
                filter_list.append(getattr(cls, key) > value[3:])
            elif value.startswith('gte:'):
                filter_list.append(getattr(cls, key) >= value[4:])
            elif value.startswith('eq:'):
                filter_list.append(getattr(cls, key) == value[3:])
            elif value.startswith('neq:'):
                filter_list.append(getattr(cls, key) != value[4:])
            elif value.startswith('lt:'):
                filter_list.append(getattr(cls, key) < value[3:])
            elif value.startswith('lte:'):
                filter_list.append(getattr(cls, key) <= value[4:])
            elif value.startswith('in:'):
                try:
                    filter_list.append(getattr(cls, key).in_(list(value[3:].split(','))))
                except Exception as e:
                    LOG.error(f'{type(cls).__name__} get_list : build filter : {str(e)}')
            else:
                filter_list.append(getattr(cls, key) == value)
        else:
            filter_list.append(getattr(cls, key) == value)

    @classmethod
    def get_list(cls, query_args=None):
        """
        Get object list from DB
        optionally with sort, filter or limit number of records.
        :param query_args: query args
        :return:
        """
        objects = []
        if cls.table_exist():
            filter_list = []
            if query_args:
                for key in query_args:
                    value = query_args.get(key)
                    if hasattr(cls, key):
                        cls._set_filter(filter_list, key, value)
            try:
                if filter_list:
                    objects = cls.query.filter(*filter_list).order_by(cls.id).all()
                else:
                    objects = cls.query.all()
            except Exception as e:
                LOG.error(f'{type(cls).__name__} get list error: {str(e)}')
        return objects

    @classmethod
    def get(cls, **kwargs):
        query_args = dict(**kwargs)
        object = cls.get_list(query_args)
        if object:
            if 1 < len(object):
                LOG.warning(f'{cls.__name__} : get has {len(object)} objects')
            object = object[0]
        else:
            object = None
        return object

    def __repr__(self):
        return '<%s %s>' % (type(self).__name__, str(self.id))

    def create(self, commit: bool = True):
        """
        Create object in DB
        :return:
        """
        try:
            db.session.add(self)
            if commit:
                db.session.commit()
        except Exception as e:
            print(f'Create {type(self).__name__} Error : {str(e)}')
            LOG.error(f'base object create: error - {str(e)}')
            raise my_exception.MyException(str(e))

    def update(self, commit: bool = True):
        """
        Update an image
        :return:
        """
        try:
            if commit:
                db.session.commit()
        except Exception as e:
            print(f'Update {type(self).__name__} Error : {str(e)}')
            LOG.error(f'base object update: error - {str(e)}')
            raise my_exception.MyException(str(e))

    def delete(self, commit: bool = True):
        """Delete object from DB"""
        try:
            db.session.delete(self)
            if commit:
                db.session.commit()
        except Exception as e:
            print(f'Delete {type(self).__name__} Error : {str(e)}')
            LOG.error(f'base object delete: error - {str(e)}')
            raise my_exception.MyException(str(e))

    @classmethod
    def delete_all(cls):
        try:
            if cls.table_exist():
                cls.query.delete()
                db.session.commit()
        except Exception as e:
            print(str(e))

    @staticmethod
    def commit():
        db.session.commit()

    def get_details(self):
        js = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                js[k] = v
        return js
