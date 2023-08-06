import sys

sys.path.append("..")

from database import TweetResultDAO
from database.PasswordUtils import hash_password

from flask import session, url_for, request, render_template, Flask
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from flask_app.forms import LoginForm, RegistrationForm, AddForm, TermsForm, ScrapeSingleTermTestForm
from scraper import Scraper
from util import merge_status_dict


def setup_http_routes(app: Flask, scraper: Scraper, tweetResultDAO: TweetResultDAO):
    from database.User import User

    @app.context_processor
    def inject_debug():
        return dict(debug=app.debug)

    @app.route('/')
    def index():
        # This code demonstrates how to use the session to store information on a user-by-user basis.
        # This can be removed later.
        data = {}
        # If user is logged in,
        if current_user.is_authenticated:

            if 'index_views' not in session:
                session['index_views'] = 0

            # They have viewed the index page 1 more time.
            session['index_views'] += 1
            data['index_views'] = session['index_views']

        return render_template('index.html', **data)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route("/success", methods=['GET', 'POST'])
    def success():
        return "Whatever you just tried worked. Congrats :)"

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Log a user in."""

        if current_user.is_authenticated == True:
            return redirect(url_for('index'))

        form = LoginForm()

        if request.method == 'POST':
            # If the form is valid,
            if form.validate():
                # Retrieve a user by email.
                check_user = User.objects(email=form.email.data).first()
                # If a user by that email exists,
                if check_user:
                    # If their hashed password matches the submitted hashed password, they have the correct creds.
                    if check_password_hash(check_user['passwordHash'], form.password.data):
                        login_user(check_user)
                        return redirect(url_for('index'))

        return render_template('forms/login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Register a new user."""
        form = RegistrationForm()
        if request.method == 'POST':
            if form.validate():
                existing_user = User.objects(email=form.email.data).first()
                if existing_user is None:
                    hashpass = hash_password(form.password.data)
                    new_user = User(form.email.data, hashpass).save()
                    login_user(new_user)
                    return redirect(url_for('index'))

        return render_template('forms/register.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        """Logs a user out."""
        logout_user()
        session.clear()
        return redirect(url_for('index'))

    @app.route('/database')
    @login_required
    def database():
        return render_template('database.html')

    @app.route('/add')
    def add():
        form = AddForm()
        return render_template('forms/test_add_numbers.html', form=form, number_result=2 + 2)

    @app.route('/scrape_multiple_terms', methods=("GET", "POST"))
    @login_required
    def scrape_multiple_terms():
        data = {}
        tweets = {}
        form = TermsForm(subdirs=tweets)
        terms_list = []

        if form.validate_on_submit():

            # For all fields,
            for datum in form.terms.data:
                # Get the user's terms and amounts
                terms = datum['term']
                terms_list.append(terms)
                amount = datum['amount']

                # Merge it with the tweets we already have.
                tweets = merge_status_dict(tweets, scraper.scrape_terms(terms=[terms], count=amount))

        allJSON = []
        for term in terms_list:
            for result in tweets[term]:
                allJSON.append(result.serialize())

        if current_user.is_authenticated:
            session['tweets_bag'] = allJSON

            if len(session['tweets_bag']) > 0 :
                print("Sample of a tweet for the user to edit:")
                print(session['tweets_bag'][0]['data']['full_text'])
                print("Tag: " + session['tweets_bag'][0]['tags'][0])
                print("Relevancy: " + session['tweets_bag'][0]['relevancy'][0])

            data['tweets_bag'] = allJSON

        return render_template("forms/scrape_multiple_terms.html", form=form, tweets=tweets, **data)

    @app.route('/scrape_single_term', methods=("GET", "POST"))
    @login_required
    def scrape_single_term():
        form = ScrapeSingleTermTestForm()

        tweets = None

        if form.validate_on_submit():
            tweets = scraper.scrape_terms(terms={form.term.data}, count=form.amount.data)

            # TODO Remove this once the jQuery Tweet editing is finished as it will no longer be needed.
            if form.saveToDatabase.data == True:
                tweetResultDAO.save_tweetresult_dict(tweets)

        return render_template('forms/scrape_single_term.html', form=form, tweets=tweets)
