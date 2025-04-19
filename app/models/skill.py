from app import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    proficiency = db.Column(db.Integer, nullable=False)  # 1-100
    category = db.Column(db.String(50))  # Programming, Design, Soft Skills, etc.