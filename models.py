from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from extensions import db 
    

class User (UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable = False, unique=True)
    username = db.Column(db.String(30), nullable = False, unique=True)
    hashed_password = db.Column(db.String(255), nullable = False)
    is_verified = db.Column(db.Boolean, nullable = False, default=False)
    verification_token = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password, method="pbkdf2")

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password, method="pbkdf2")

class Listing(db.Model):

    __tablename__ = "listings"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

# will have to manually populate and create communities within db, users and other processes should NOT be able to access CRUD methods 
# class Community(db.Model):
#     __tablename__ = "community"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     # users: Mapped[List]
