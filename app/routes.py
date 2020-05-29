import requests
from flask import render_template, redirect, url_for, flash

import app.firebase_submit as firebase
from app import app, firebase_config
from app import app_config
from app.forms import KudosForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='kudobox')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', firebase_config=firebase_config)


@app.route('/kudos', methods=['GET', 'POST'])
def kudos():
    form = KudosForm()
    if form.validate_on_submit():
        access_token = form.token_tag.data
        try:
            firebase.submit(form.sender.data, form.receiver.data, form.text.data, access_token)
            flash("Your kudo was successfully submitted.")
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError:  # probably unauthenticated
            flash("There was an error submitting your kudo.")
            flash(f"Did you register and confirm your email?")
            flash(f"Does your email end with @{app_config['company']}?")
            flash(f"Did you try logging in again?")
            return render_template('kudos.html', form=form, firebase_config=firebase_config)
    return render_template('kudos.html', form=form, firebase_config=firebase_config)
