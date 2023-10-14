"""This module is used to manage the Flask app."""
from flask_migrate import upgrade, migrate, init, stamp

from app import create_app, db


def deploy():
    """
    Run deployment tasks.

    This function creates a Flask app, initializes the app context, and creates the database tables.
    It then migrates the database to the latest revision, stamps the migration, and upgrades the database.
    """

    app = create_app()
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    init()
    stamp()
    migrate()
    upgrade()


if __name__ == "__main__":
    deploy()
