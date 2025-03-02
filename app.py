import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import logging
from logging.config import dictConfig

# Configure logging
dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
})

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configuration des paramètres d'upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mobi'}

# Fonction pour vérifier si l'extension du fichier est autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# In-memory user storage for demonstration (replace with a database in production)
users = {}
users['test'] = generate_password_hash('test')
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

# Route pour l'upload de fichiers
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('main'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Log the username and password (for debugging purposes only)
        app.logger.debug(f"Attempting to log in with Username: {username}, Password: {password}")
        user_name = username.strip()
        passwd = password.strip()
        app.logger.debug(f"list of Username: {users}")
        try:
            t = check_password_hash(users[user_name], passwd)
        except KeyError:
            app.logger.warning(f"Failed login attempt for Username: {user_name}")
            flash('Invalid username or password')
            return render_template('login.html')
        app.logger.debug(f"hash {t}")
        # Check if user exists and password is correct
        if user_name in users and check_password_hash(users[user_name], passwd):
            user = User(user_name)
            login_user(user)
            app.logger.info(f"User {user_name} logged in successfully.")
            return redirect(url_for('main'))  # Redirect to main screen on success
        else:
            app.logger.warning(f"Failed login attempt for Username: {user_name}")
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/')
@app.route('/main')
@login_required
def main():
    # Liste des fichiers dans le dossier d'uploads
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
    return render_template('main.html', files=files)
    #return render_template('main.html', username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    app.logger.info(f"User {current_user.id} logged out.")
    return redirect(url_for('login'))

# Route pour télécharger les fichiers
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == '__main__':
    # Sample user for demonstration (username: test, password: test)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
