from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#from base64 import b64encode
import os
import sys
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash



WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'wine.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['UPLOAD_FOLDER'] = '.\static\db_wines'
app.config['SECRET_KEY'] = 'your_random_secret_key_here'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#app.jinja_env.filters['b64encode'] = b64encode
# Database 
class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

class FeaturedWine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'), nullable=False)
    wine = db.relationship('Wine', backref=db.backref('featured', uselist=False))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Define allowed image file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

@app.before_request
def create_user():
    user = User.query.filter_by(username='username').first()
    # Example user creation code within application context
    if user is None:
        hashed_password = generate_password_hash('zxc123457')
        new_user = User(username='username', password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    else:
        pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Verifying password
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('list_wine'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

'''
@app.route('/register', methods=['POST'])
def register():
    # Assume form data is being correctly gathered into username, password variables
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    
    new_user = User(username=username, password_hash=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return "User registered successfully!"
    except IntegrityError:
        db.session.rollback()  # Roll back the transaction to keep the session clean
        return "This username is already taken. Please choose another one."
'''

@app.route('/add_wine', methods=['GET', 'POST'])
@login_required
def add_wine():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        
        if 'image' not in request.files:
            return "Error: No image provided."
        
        image_file = request.files['image']

        if image_file.filename == '':
            return "Error: No selected image file."
        
        if image_file and allowed_file(image_file.filename):
            filename = image_file.filename
            print(filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            ####################
            image_path = 'db_wines/'+filename
            ####################
            print(image_path)
            
            new_wine = Wine(name=name, description=description, price=price, image_path=image_path)
            db.session.add(new_wine)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "Error: Invalid image file type."

    return render_template('add_wine.html')

@app.route('/edit_wine/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_wine(id):
    wine = Wine.query.get_or_404(id)
    if request.method == 'POST':
        wine.name = request.form['name']
        wine.description = request.form['description']
        wine.price = float(request.form['price'])
        print('123', request.files)
        if 'image' not in request.files:
            return "Error: No image provided."
        
        image_file = request.files['image']

        if image_file.filename == '':
            return "Error: No selected image file."
        
        if image_file and allowed_file(image_file.filename):
            filename = image_file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            ####################
            image_path = 'db_wines/'+filename
            ####################
            print(image_path)
            
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "Error: Invalid image file type."
    
    return render_template('edit_wine.html', wine=wine)

@app.route('/wine_delete/<int:id>', methods=['POST'])
@login_required
def delete_wine(id):
    wine = Wine.query.get_or_404(id)
    db.session.delete(wine)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/list_wine')
@login_required
def list_wine():
    wines = Wine.query.all()
    return render_template('list_wines.html', wines=wines)

@app.route('/')
def index():
    a = Wine.query.all()
    return render_template('index.html', wines=a)



if __name__ == '__main__':
    app.run(debug=True)
