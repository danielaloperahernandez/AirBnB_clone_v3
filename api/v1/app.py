#!/usr/bin/python3
"""Module for Flask REST_API"""
from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views
from os import getenv
from flask import make_response, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def closedb(db_close):
    """Closes db session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Create a handler for 404 errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
