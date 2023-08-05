import os
import sys
from win32print import AddForm

from flask_login import login_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from util import merge_status_dict

sys.path.append("..")


from flask import Flask, render_template, url_for, request
from scraper import Scraper

current_folder = os.path.abspath(os.path.dirname(__file__))
static_folder = os.path.join(current_folder, 'static')
template_folder = os.path.join(current_folder, 'templates')

app = Flask(__name__, static_url_path='/static', template_folder=template_folder, static_folder=static_folder)

from flask_app.forms import *
from database.User import User

from twitter import TwitterAuthentication

scraper = Scraper(twitter_authentication=TwitterAuthentication.autodetect_twitter_auth())


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/success")
def success():
    return "Whatever you just tried worked. Congrats :)"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                new_user = User(form.email.data, hashpass).save()
                login_user(new_user)
                return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/add')
def add():
    form = AddForm()
    return render_template('dynamic_form.html', form = form, number_result = 2+2)


@app.route('/newForm', methods=['GET', 'POST'])
def newForm():
    user_subdirs = {}
    form = SubDirsForm(subdirs = user_subdirs)
    flash("You're are now live!")
    return render_template('dynamic_form.html', title=('Home'), form=form)


@app.route('/scrape_multiple_terms', methods=("GET", "POST"))
def scrape_multiple_terms():
    form = TermsForm()

    tweets = {}

    if form.validate_on_submit():

        # For all fields,
        for datum in form.terms.data:
            # Get the user's terms and amounts
            terms = datum['term']
            amount = datum['amount']

            # Merge it with the tweets we already have.
            tweets = merge_status_dict(tweets, scraper.scrape_terms(terms=[terms], count=amount))

    return render_template("dynamic_form.html", form=form, tweets=tweets)


@app.route('/scrape_single_term', methods=("GET", "POST"))
def scrape_single_term():
    form = ScrapeSingleTermTestForm()

    tweets = None

    if form.validate_on_submit():
        tweets = scraper.scrape_terms(terms={form.term.data}, count=form.amount.data)

    return render_template('scrape_single_term.html', form=form, tweets=tweets)
