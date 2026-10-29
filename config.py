
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "change-this-secret-before-deployment"
    )

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:@127.0.0.1:3306/clinicalcase"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
