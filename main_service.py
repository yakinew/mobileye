from my_log import LOG
from service import MyService

if __name__ == '__main__':
    try:
        LOG.info(f'Service : Start!')
        my_service = MyService()
        my_service.run()
    except Exception as e:
        LOG.error(f'Service : {e}')
