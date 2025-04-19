from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.project import Project
from app.models.skill import Skill
from app.models.about import AboutMe
from app.models.message import ContactMessage
from app import db, mail
from flask_mail import Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    projects = Project.query.order_by(Project.date_added.desc()).limit(3).all()
    skills = Skill.query.all()
    about = AboutMe.query.first()
    return render_template('index.html', projects=projects, skills=skills, about=about)

@main_bp.route('/about')
def about():
    about_info = AboutMe.query.first()
    return render_template('about.html', about=about_info)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')

        contact_msg = ContactMessage(name=name, email=email, subject=subject, content=content)
        db.session.add(contact_msg)
        db.session.commit()

        # Send email notification
        try:
            msg = Message(
                subject=f"New Portfolio Contact: {subject}",
                recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
                body=f"From: {name} ({email})\n\n{content}"
            )
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            current_app.logger.error(f"Mail send error: {e}")
            flash('Your message was saved, but email notification failed.', 'warning')

        return redirect(url_for('main.contact'))

    return render_template('contact.html')