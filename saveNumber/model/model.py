
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
