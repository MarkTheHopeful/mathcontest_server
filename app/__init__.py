from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.db_manager import DBManager
from app.game_manager import GameManager
from app import models

dbm = DBManager(db, models)
gm = GameManager(dbm)

from app import routes
