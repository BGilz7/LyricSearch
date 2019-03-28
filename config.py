# hold all configuration variables for this application here
# should not be uploaded to github with sensitive information
# when uploading to heroku, use import os .get() methods
import os


# define the root/base of this project folder
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # secret key is necessary for forms in flask, it is a security measure to protect against attacks like CSRF
    # it should never be given out, and should be something that is difficult to break
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # uri for sql lite database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
