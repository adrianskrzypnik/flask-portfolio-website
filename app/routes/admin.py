from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from app.models.skill import Skill
from app.models.message import ContactMessage
from app.models.about import AboutMe

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Helper function to check admin status
def admin_required(func):
    @login_required
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    decorated_view.__name__ = func.__name__
    return decorated_view

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

# Project management routes
@admin_bp.route('/projects')
@admin_required
def admin_projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

@admin_bp.route('/project/new', methods=['GET', 'POST'])
@admin_required
def new_project():
    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            image_url=request.form.get('image_url'),
            github_url=request.form.get('github_url'),
            live_url=request.form.get('live_url'),
            technologies=request.form.get('technologies')
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.admin_projects'))

    return render_template('admin/project_form.html')

@admin_bp.route('/project/edit/<int:project_id>', methods=['GET', 'POST'])
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.image_url = request.form.get('image_url')
        project.github_url = request.form.get('github_url')
        project.live_url = request.form.get('live_url')
        project.technologies = request.form.get('technologies')
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.admin_projects'))

    return render_template('admin/project_form.html', project=project)

@admin_bp.route('/project/delete/<int:project_id>', methods=['POST'])
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.admin_projects'))

# Skill management routes
@admin_bp.route('/skills')
@admin_required
def admin_skills():
    skills = Skill.query.all()
    return render_template('admin/skills.html', skills=skills)

@admin_bp.route('/skill/new', methods=['GET', 'POST'])
@admin_required
def new_skill():
    if request.method == 'POST':
        skill = Skill(
            name=request.form.get('name'),
            proficiency=int(request.form.get('proficiency')),
            category=request.form.get('category')
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin.admin_skills'))

    return render_template('admin/skill_form.html')

@admin_bp.route('/skill/edit/<int:skill_id>', methods=['GET', 'POST'])
@admin_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if request.method == 'POST':
        skill.name = request.form.get('name')
        skill.proficiency = int(request.form.get('proficiency'))
        skill.category = request.form.get('category')
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('admin.admin_skills'))

    return render_template('admin/skill_form.html', skill=skill)

@admin_bp.route('/skill/delete/<int:skill_id>', methods=['POST'])
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin.admin_skills'))

# Message management routes
@admin_bp.route('/messages')
@admin_required
def admin_messages():
    msgs = ContactMessage.query.order_by(ContactMessage.date_sent.desc()).all()
    return render_template('admin/messages.html', messages=msgs)

@admin_bp.route('/message/<int:message_id>')
@admin_required
def view_message(message_id):
    msg = ContactMessage.query.get_or_404(message_id)
    msg.read = True
    db.session.commit()
    return render_template('admin/message_detail.html', message=msg)

# About management route
@admin_bp.route('/about', methods=['GET', 'POST'])
@admin_required
def admin_about():
    about = AboutMe.query.first()
    if not about:
        about = AboutMe(content="Add your bio here!", resume_url="", linkedin_url="", github_url="", twitter_url="")
        db.session.add(about)
        db.session.commit()

    if request.method == 'POST':
        about.content = request.form.get('content')
        about.resume_url = request.form.get('resume_url')
        about.linkedin_url = request.form.get('linkedin_url')
        about.github_url = request.form.get('github_url')
        about.twitter_url = request.form.get('twitter_url')
        db.session.commit()
        flash('About information updated successfully!', 'success')
        return redirect(url_for('admin.admin_about'))

    return render_template('admin/about_form.html', about=about)