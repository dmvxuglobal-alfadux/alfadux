from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_dev_only'

# Database Configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration (Gmail Example - Requires App Password)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# Clean password just in case (remove spaces)
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS').replace(" ", "") if os.environ.get('EMAIL_PASS') else None
# Explicitly set default sender to avoid 550 errors
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

db = SQLAlchemy(app)
mail = Mail(app)

# Database Model
class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    program = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Inquiry('{self.full_name}', '{self.email}', '{self.program}')"

# Create tables within app context
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', page='home')

@app.route('/mba-india')
def mba_india():
    return render_template('mba_india.html', page='mba-india')

@app.route('/global-mba')
def global_mba():
    return render_template('global_mba.html', page='global-mba')

@app.route('/dba')
def dba_overview():
    return render_template('dba_overview.html', page='dba')

@app.route('/dba/golden-gate')
def golden_gate():
    return render_template('universities/golden_gate.html', page='dba')

@app.route('/dba/edgewood')
def edgewood():
    return render_template('universities/edgewood.html', page='dba')

@app.route('/dba/rushford')
def rushford():
    return render_template('universities/rushford.html', page='dba')

@app.route('/dba/esgci')
def esgci():
    return render_template('universities/esgci.html', page='dba')

@app.route('/dba/ssbm')
def ssbm():
    return render_template('universities/ssbm.html', page='dba')

@app.route('/mentors')
def mentors():
    return render_template('mentors/index.html', page='mentors')

@app.route('/mentors/apply')
def mentor_apply():
    return render_template('mentors/apply.html', page='mentors')

@app.route('/mentors/apply-submit', methods=['POST'])
def mentor_apply_submit():
    try:
        data = request.form
        
        # Combine extra fields into the message for storage
        full_message = f"""
        LinkedIn: {data.get('linkedin')}
        Current Role: {data.get('role_company')}
        
        Motivation:
        {data.get('message')}
        """

        # Save to Database (using existing schema)
        new_inquiry = Inquiry(
            full_name=data.get('full_name'),
            email=data.get('email'),
            mobile_number=data.get('mobile_number'),
            program='Mentor Application', # Hardcoded program type
            message=full_message
        )
        db.session.add(new_inquiry)
        db.session.commit()
        
        print(f"✅ Saved Mentor Application to DB: {new_inquiry}")

        # Send Email Notification
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            print(f"📧 Attempting to send email from {app.config['MAIL_USERNAME']}...")
            msg = Message('New MENTOR Application', recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"""
            New MENTOR Application Received:
            
            Name: {new_inquiry.full_name}
            Email: {new_inquiry.email}
            Mobile: {new_inquiry.mobile_number}
            
            LinkedIn: {data.get('linkedin')}
            Current Role: {data.get('role_company')}
            
            Motivation/Message:
            {data.get('message')}
            """
            try:
                mail.send(msg)
                print("✅ Email sent successfully.")
            except Exception as mail_error:
                print(f"❌ Email Failed: {mail_error}")
        else:
            print("⚠️ Email credentials not found. Skipping email sending.")

        flash('Application submitted successfully. Our team will review your profile.', 'success')
        return redirect(url_for('mentor_apply'))
        
    except Exception as e:
        print(f"❌ Error processing mentor application: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Something went wrong. Please try again later. (Error: {str(e)})', 'error')
        return redirect(url_for('mentor_apply'))



@app.route('/contact', methods=['POST'])
def contact_submit():
    try:
        data = request.form
        
        # Save to Database
        # Save to Database
        # Map fields: 'name' from form -> 'full_name' in DB, 'phone' -> 'mobile_number'
        full_name = data.get('name') or data.get('full_name')
        mobile_number = data.get('phone') or data.get('mobile_number')

        new_inquiry = Inquiry(
            full_name=full_name,
            email=data.get('email'),
            mobile_number=mobile_number,
            program=data.get('program'),
            message=data.get('message')
        )
        db.session.add(new_inquiry)
        db.session.commit()
        
        print(f"✅ Saved to DB: {new_inquiry}")

        # Send Email Notification
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            print(f"📧 Attempting to send email from {app.config['MAIL_USERNAME']}...")
            msg = Message('New Admission Inquiry', recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"""
            New Inquiry Received:
            
            Name: {new_inquiry.full_name}
            Email: {new_inquiry.email}
            Mobile: {new_inquiry.mobile_number}
            Program: {new_inquiry.program}
            Message: {new_inquiry.message}
            """
            try:
                mail.send(msg)
                print("✅ Email sent successfully.")
            except Exception as mail_error:
                print(f"❌ Email Failed: {mail_error}")
                # We don't re-raise here so the user still gets a success message if DB save worked
        else:
            print("⚠️ Email credentials not found. Skipping email sending.")

        flash('Thank you for your interest. An admissions advisor will contact you shortly.', 'success')
        return redirect(url_for('home', _anchor='contact'))
        
    except Exception as e:
        print(f"❌ Error processing inquiry: {e}")
        # Print full traceback for debugging
        import traceback
        traceback.print_exc()
        flash(f'Something went wrong. Please try again later. (Error: {str(e)})', 'error')
        return redirect(url_for('home', _anchor='contact'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
