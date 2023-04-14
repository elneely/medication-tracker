import unittest
from app import app, db
from app.models import User, Medication, Doctor, Pharmacy
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

