from application import db
from sqlalchemy import LargeBinary


class Celebrity(db.Model):
    __tablename__ = 'celebrity'
    celebrity_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    celebrity_name = db.Column(db.String(500), nullable=False, unique=True)
    category = db.Column(db.String(500), nullable=False, unique=True)
    Insta = db.Column(db.String(500), nullable=False, unique=True)
    yt = db.Column(db.String(500), nullable=False, unique=True)
    twitter = db.Column(db.String(500), nullable=False, unique=True)
    profile = db.Column(db.LargeBinary)
