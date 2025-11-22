from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')
    api_token = db.Column(db.String(100), unique=True)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

def init_db(app):
    with app.app_context():
        db.create_all()
        
        # Seed data
        if not User.query.filter_by(username='jdoe').first():
            jdoe = User(
                username='jdoe',
                password_hash='password', # Plaintext for demo as per spec
                email='jdoe@corp.local',
                role='user',
                api_token='user-session-token-123'
            )
            db.session.add(jdoe)
            db.session.commit()
