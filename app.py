from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/')
def index():
    return 'Backend: You are viewing the backend.'

@app.route('/api/request', methods=['GET'])
def send_request():
    # You can add any necessary logic here
    return '200 OK'

# Ensure Flask runs only when executed directly, not when imported
if __name__ == '__main__':
    # Use a production-ready server like gunicorn with awsgi adapter
    from gunicorn.app.base import BaseApplication
    from awsgi import flask as awsgi_flask

    class FlaskApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.application = app
            self.options = options or {}
            super(FlaskApplication, self).__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '0.0.0.0:8000',  # Bind to port 8000
        'workers': 4,  # Use 4 worker processes
    }

    application = FlaskApplication(app, options)
    application.run()

