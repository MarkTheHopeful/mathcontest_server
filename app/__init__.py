from flask import Flask
from app.extensions import db, migrate, dbm, gm
from app import models
from config import Config


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    dbm.init_db(db, models)
    gm.init_dbm(dbm)


app = create_app()
from app import routes  # FIXME: ugly.
