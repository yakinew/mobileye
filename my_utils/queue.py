import json
from multiprocessing.connection import Client, Listener

import my_exception
from my_log import LOG
from my_utils.settings import get_hostname, get_authkey, get_internal_port


class MyQueue:
    CLOSE_CONNECTION_MSG = 'close connection'
    authkey = b''
    hostname = ''
    internal_port = 0
    __listener = None

    @classmethod
    def __set_auth(cls):
        if not cls.hostname:
            cls.hostname = get_hostname()
        if not cls.authkey:
            cls.authkey = get_authkey()
        if not cls.internal_port:
            cls.internal_port = get_internal_port()

    @classmethod
    def send(cls, action: str, data: dict = None):
        """
        Send a message to the server
        :param action: The action to do in the subprocess
        :param data: The data for this action
        :return:
        """
        cls.__set_auth()

        msg = {'action': action, 'data': data}
        msg_str = json.dumps(msg)
        try:
            conn = Client((cls.hostname, cls.internal_port), authkey=cls.authkey)
            conn.send(msg_str)
            conn.send(cls.CLOSE_CONNECTION_MSG)
            conn.close()
            LOG.debug(f'MyQueue : Success to send msg : {action} {data}!')
        except ConnectionRefusedError as e:
            LOG.error(f'MyQueue : Send : {e}')
            raise my_exception.InternalCommunication()
        except Exception as e:
            LOG.error(f'MyQueue : Send : {e}')
            raise my_exception.MyException(f'MyQueue Send : {e}')

    @classmethod
    def listener(cls):
        """
        Open listener
        :return:
        """
        cls.__set_auth()
        if not cls.__listener:
            cls.__listener = Listener((cls.hostname, cls.internal_port), authkey=cls.authkey)

    @classmethod
    def get(cls):
        """
        Get a single message from client
        :return:
        """
        action, data = '', None

        # Accept new connection:
        conn = cls.__listener.accept()

        while True:
            # Receive new message:
            msg_str = conn.recv()
            if msg_str == cls.CLOSE_CONNECTION_MSG:
                conn.close()
                break

            if action:
                LOG.warning(f'MyQueue get : Got more then one message at a time ({action})')

            # Parse the message:
            LOG.debug(f'MyQueue : received : {msg_str}')
            msg = json.loads(msg_str)
            action = msg['action']
            data = msg['data']

        return action, data
