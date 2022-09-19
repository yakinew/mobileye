from app import app
from web_server.rest import app as app_api

_apps = (app_api,)
for _app in _apps:
    app.register_blueprint(_app)

if __name__ == '__main__':
    app.run(port=8081)
