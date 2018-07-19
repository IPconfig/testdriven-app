# services/users/manage.py

from flask.cli import FlaskGroup
from project import app

# Create a new FlaskGroup instance to extend normal CLI with commands related to the Flask app
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
