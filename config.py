class ApplicationConfig:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234567890@localhost/test_react'
