# services/users/manage.py

from flask.cli import FlaskGroup
from project import app, db

# Create a new FlaskGroup instance to extend normal CLI with commands related to the Flask app
cli = FlaskGroup(app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    cli()
