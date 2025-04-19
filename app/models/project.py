from app import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    live_url = db.Column(db.String(200))
    technologies = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)