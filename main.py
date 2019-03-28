from app import app, db
from app.models import User, Email

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Email': Email, 'User': User, 'Favorites': Favorites }
