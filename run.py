from app import app as application
from src.database import db

db.init(application)


@application.before_first_request
def create_tables():
    db.create_all()
