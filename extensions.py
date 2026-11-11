#please have any shared dependencies here 
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

db = SQLAlchemy()

# async def verifyEmail(email: str):
#     if not email.lower().endswith(".edu"):
#         return 400
#     return 