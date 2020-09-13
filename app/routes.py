from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, abort
from app.forms import LoginForm, RegistrationForm, SearchForm, PostForm
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.models import User, Post
from app import app, db
import os

ALLOWED_EXTENSIONS = set(['png','jpeg','gif', 'jpg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        if form.search_feld.data == "":
                return redirect(url_for('search',search_stuff=" "))
        search_thing = form.search_feld.data.replace("/","%2F")
        return redirect(url_for('search',search_stuff=search_thing))
    return render_template('home.html',title="Home", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/search/<search_stuff>', methods=['GET','POST'])
def search(search_stuff):
    search_stuff = search_stuff.replace("%2F","/")
    for p in Post.query.all():
        if search_stuff.lower() == p.name.lower():
            i = p.path
            return render_template('search.html',title="search", search_word=search_stuff, bilde=i)
    return render_template('search.html',title="search", search_word=search_stuff)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        if allowed_file(form.file.data.filename):
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user = User.query.filter_by(username=current_user.username).first_or_404()
            post = Post(name=form.name.data, path=url_for('static',filename='bilder/'+filename), author=user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('post.html',title="post", form=form, post=Post, nummer=0)
