from app import app, db
from flask import render_template, url_for, redirect, flash, jsonify, request
import requests
from app.forms import LyricForm, EmailForm, LoginForm, RegisterForm
from app.models import User, Favorites
from flask_login import current_user, login_user, logout_user, login_required
# from app.temp_data import songs as song_data
import pandas as pd
import os
# define the root/base of this project folder
BASEDIR = os.path.abspath(os.path.dirname(__file__))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    # songs = song_data
    songs = { 'result': [] }

    form = LyricForm()

    if form.validate_on_submit():
        search = form.lyrics.data

        response = "https://api.audd.io/findLyrics/?q={}".format(search)

        songs = requests.get(response).json()
        print(songs)

    return render_template('index.html', title='Lyrics', songs=songs['result'], form=form)

# @app.route('/t', methods=['GET', 'POST'])
# @app.route('/test', methods=['GET', 'POST'])
# def index2():
#
#     html = []
#
#     form = LyricForm()
#
#     if form.validate_on_submit():
#         search = form.lyrics.data
#
#         # load lyrics from csv into pd df
#         df = pd.read_csv(BASEDIR + '/static/data/lyrics.csv')
#
#         df.fillna('N/A')
#         songs = df[df['lyrics'].str.contains(search, na=False)]
#
#         html = songs.to_html()
#
#
#     return render_template('test.html', title='Lyrics', html=html, form=form)

@app.route('/add_favorite/<song_id>/<title>/<artist>', methods=['GET'])
def add_favorite(song_id, title, artist):
    saved_song = Favorites(song_id=song_id, artist=artist, title=title, user_id=current_user.id)

    # add post variable to database stage, then commit
    db.session.add(saved_song)
    db.session.commit()

    flash('Song saved!')

    return redirect(url_for('index', username=current_user.username))

@app.route('/remove_favorite/<song_id>', methods=['GET'])
def remove_favorite(song_id):
    saved_song = Favorites.query.filter_by(song_id=song_id).first()

    db.session.delete(saved_song)
    db.session.commit()


    return redirect(url_for('favorites', username=current_user.username))

@login_required
@app.route('/favorites/<username>', methods=['GET', 'POST'])
def favorites(username):

    # query database for proper person
    person = User.query.filter_by(username=username).first()

    songs = Favorites.query.filter_by(user_id=person.id).all()

    return render_template('favorites.html', title='Favorites', person=person, username=username, songs=songs)


@login_required
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is Logged in already, do not let them access this page
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))


    form = LoginForm()

    # check if form is submitted, log user in if so
    if form.validate_on_submit():
        # query the database for the user trying to log in
        user = User.query.filter_by(username=form.username.data).first()

        # if user doesnt exist, reload page and flash messages
        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect.')
            return redirect(url_for('login'))

        # if user does exist, and credentials are correct, log them in and send them to their profile page
        login_user(user, remember=form.remember_me.data)
        flash('You are now logged in!')
        return redirect(url_for('index', username=current_user.username))


    return render_template('login.html', title='Login:', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is Logged in already, do not let them access this page
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data
        )

        # set the password hash
        user.set_password(form.password.data)

        # add to stage and commit to db, then flash and return
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register:', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
