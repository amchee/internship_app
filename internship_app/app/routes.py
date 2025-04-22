from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Internship, Application
from .forms import InternshipForm, ApplicationForm
from .email_service import send_welcome_email

main = Blueprint('main', __name__)

@main.route('/')
def index():
    internships = Internship.query.all()
    return render_template('index.html', internships=internships)

@main.route('/post', methods=['GET', 'POST'])
def post_internship():
    form = InternshipForm()
    if form.validate_on_submit():
        title = form.title.data
        company = form.company.data
        description = form.description.data
        
        new_internship = Internship(title=title, company=company, description=description)
        db.session.add(new_internship)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('post_internship.html', form=form)

@main.route('/apply/<int:internship_id>', methods=['GET', 'POST'])
def apply(internship_id):
    internship = db.session.get(Internship, internship_id)
    if internship is None:
        return render_template("404.html"), 404

    form = ApplicationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        
        application = Application(name=name, email=email, internship_id=internship_id)
        db.session.add(application)
        db.session.commit()

        send_welcome_email(email)

        return redirect(url_for('main.index'))
    
    return render_template('apply.html', internship=internship, form=form)
