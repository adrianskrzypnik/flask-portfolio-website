import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User
from app.models.project import Project
from app.models.skill import Skill
from app.models.about import AboutMe

@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True)
        admin.set_password('adminpassword')  # Change this in production
        db.session.add(admin)

    if not Project.query.first():
        sample_projects = [
            Project(
                title='Portfolio Website',
                description='A personal portfolio website built with Flask and Bootstrap.',
                image_url='https://via.placeholder.com/300',
                github_url='https://github.com/adrianskrzypnik/flask-portfolio-website',
                live_url='https://yourportfolio.com',
                technologies='Flask, SQLAlchemy, Bootstrap, JavaScript'
            ),
            Project(
                title='E-commerce Platform',
                description='A full-featured e-commerce platform with payment integration.',
                image_url='https://via.placeholder.com/300',
                github_url='https://github.com/yourusername/ecommerce',
                live_url='https://yourecommerce.com',
                technologies='Django, PostgreSQL, React, Stripe'
            ),
            Project(
                title='Task Management App',
                description='A collaborative task management application with real-time updates.',
                image_url='https://via.placeholder.com/300',
                github_url='https://github.com/yourusername/taskmanager',
                live_url='https://yourtaskapp.com',
                technologies='Node.js, Express, MongoDB, Socket.io'
            )
        ]

        db.session.bulk_save_objects(sample_projects)

        sample_skills = [
            Skill(name='Python', proficiency=90, category='Programming'),
            Skill(name='JavaScript', proficiency=85, category='Programming'),
            Skill(name='Flask', proficiency=88, category='Frameworks'),
            Skill(name='SQLAlchemy', proficiency=80, category='Databases'),
            Skill(name='HTML/CSS', proficiency=95, category='Frontend'),
            Skill(name='React', proficiency=75, category='Frontend'),
            Skill(name='Git', proficiency=85, category='Tools'),
            Skill(name='Docker', proficiency=70, category='DevOps')
        ]
        db.session.bulk_save_objects(sample_skills)

        about = AboutMe(
            content="I'm a passionate software developer with experience in web development, data science, and cloud computing. I love building scalable applications and solving complex problems.",
            resume_url="https://yoursite.com/resume.pdf",
            linkedin_url="https://www.linkedin.com/in/adrian-skrzypnik-3102782a4/",
            github_url="https://github.com/adrianskrzypnik",
            twitter_url="https://twitter.com/yourusername"
        )
        db.session.add(about)

    db.session.commit()
    print('Database initialized with admin user and sample data')