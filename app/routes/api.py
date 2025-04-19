from flask import Blueprint, jsonify
from app.models.project import Project
from app.models.skill import Skill

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/skills')
def api_skills():
    skills = Skill.query.all()
    return jsonify([{'name': s.name, 'proficiency': s.proficiency, 'category': s.category} for s in skills])

@api_bp.route('/projects')
def api_projects():
    projects = Project.query.all()
    return jsonify([
        {
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'image_url': p.image_url,
            'github_url': p.github_url,
            'live_url': p.live_url,
            'technologies': p.technologies,
            'date_added': p.date_added.strftime('%Y-%m-%d')
        }
        for p in projects
    ])