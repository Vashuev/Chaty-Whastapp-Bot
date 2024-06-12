from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    msg_id = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date, default=None)
    end_date = db.Column(db.Date, default=None)
    budget = db.Column(db.Float, default=0.0)
    company = db.Column(db.String(50), default='')
    job = db.Column(db.String(50), default='')
    email = db.Column(db.String(120), default='')
    otp = db.Column(db.Integer, default=None)

    def __repr__(self):
        return f"<UserProgress(user_id='{self.user_id}', msg_id={self.msg_id})>"

##################### Setter function #######################
def save_message_progress(user_id, new_msg_id):
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        user_progress.msg_id = new_msg_id
    else:
        user_progress = UserProgress(user_id=user_id, msg_id=new_msg_id)
        db.session.add(user_progress)
    db.session.commit()

# start date
def save_start_date(user_id, date):
    print(f"inside start_date = {type(date)}, value = {date}")
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        user_progress.start_date = date
    else:
        user_progress = UserProgress(user_id=user_id, start_date=date)
        db.session.add(user_progress)
    db.session.commit()

# end date
def save_end_date(user_id, date_str, is_one=False):
    print(f"inside end_date = {type(date_str)}, value = {date_str}")
    if is_one:
        parsed_date = datetime.strptime(str(date_str), '%d/%m/%Y').date()
    else:
        parsed_date = datetime.strptime(date_str, '%d/%m/%y').date()
    print(f"inside end_date = {type(parsed_date)}, value = {parsed_date}")
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        user_progress.end_date = parsed_date
    else:
        user_progress = UserProgress(user_id=user_id, end_date=parsed_date)
        db.session.add(user_progress)
    db.session.commit()


# budget
def save_budget(user_id, budget):

    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        user_progress.budget = budget
    else:
        user_progress = UserProgress(user_id=user_id, budget=budget)
        db.session.add(user_progress)
    db.session.commit()

# Company
def save_company(user_id, company):

    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        user_progress.company = company
    else:
        user_progress = UserProgress(user_id=user_id, company=company)
        db.session.add(user_progress)
    db.session.commit()

# job
def save_job(user_id, job):

    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        user_progress.job = job
    else:
        user_progress = UserProgress(user_id=user_id, job=job)
        db.session.add(user_progress)
    db.session.commit()

# email
def save_email(user_id, email):

    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        user_progress.email = email
    else:
        user_progress = UserProgress(user_id=user_id, email=email)
        db.session.add(user_progress)
    db.session.commit()

# otp
def save_otp(user_id, otp):
    user_progress = UserProgress.query.filter_by(user_id= user_id).first()
    if user_progress:
        user_progress.otp = otp
    else:
        user_progress = UserProgress(user_id=user_id, otp=otp)
        db.session.add(user_progress)
    db.session.commit()

##################### getter function ################
def get_message_id(user_id):
    # Query the UserProgress table for the given user_id
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        return user_progress.msg_id
    else:
        # If user_id doesn't exist in the database, return 0
        return 0

def get_start_date(user_id):
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress and user_progress.start_date:
        return user_progress.start_date.strftime('%d/%m/%Y')
    else:
        return 'No date available'
    
def get_end_date(user_id):
    # Query the UserProgress table for the given user_id
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress and user_progress.end_date:
        return user_progress.end_date.strftime('%d/%m/%Y')
    else:
        # Return a placeholder string if the date is not available
        return 'No date available'
    
def get_budget(user_id):
    # Query the UserProgress table for the given user_id
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        return user_progress.budget
    else:
        # If user_id doesn't exist in the database, return 0
        return 0

def get_company(user_id):
    # Query the UserProgress table for the given user_id
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        return user_progress.company
    else:
        # If user_id doesn't exist in the database, return 0
        return 0

def get_job(user_id):
    # Query the UserProgress table for the given user_id
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        return user_progress.job
    else:
        # If user_id doesn't exist in the database, return 0
        return 0

def get_email(user_id):
    # Query the UserProgress table for the given user_id
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        return user_progress.email
    else:
        # If user_id doesn't exist in the database, return 0
        return 0

def get_otp(user_id):
    user_progress = UserProgress.query.filter_by(user_id=user_id).first()
    if user_progress:
        return user_progress.otp
    else:
        return 000000

def verfity_otp(user_id, user_response):
    try:
        if get_otp(user_id) == int(user_response):
            return True
        return False
    except:
        return False
    
####################### delete the user ####################

def delete_user(user_id):
    user = UserProgress.query.filter_by(user_id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return f"User with id {user_id} deleted successfully."
    else:
        return f"User with id {user_id} does not exist."