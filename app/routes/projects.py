from flask import Blueprint, render_template
from app.models.project import Project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.date_added.desc()).all()
    return render_template('projects.html', projects=all_projects)

@projects_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)