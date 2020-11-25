from flask import request, render_template, flash, jsonify
from flask import session, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from .forms import *

from flask import current_app as app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
        return render_template("about.html")


@app.route("/signup/", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, password = form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("This Username already exists in the system! Please login or choose another username")
            return redirect(url_for("signup", form = form))
        finally:
            db.session.close()
        return redirect(url_for("login"))
    return render_template("signup.html", form = form)

@app.route("/login/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data, password = form.password.data).first()
        if user is None:
            flash("Wrong Credentials. Please Try Again.")
            return redirect(url_for("login", form = form))
        else:
            login_user(user)
            return redirect(url_for("decks"))
    return render_template("login.html", form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/decks/")
@login_required
def decks():
    decks = db.session.query(Deck).filter_by(created_by = current_user.id)
    return render_template("decks.html", decks = decks)
    
@app.route("/study/<deck_ref>", methods=["GET"])
@login_required
def study(deck_ref):
    session['count'] = 0
    session['deck_r'] = deck_ref
    cards = db.session.query(Card).filter_by(created_by = deck_ref)
    if cards.count() > 0:
        return render_template("study.html", cards = cards, index = 0)

    flash("This Deck has no Cards. Add a Card to it.")
    return redirect(url_for("decks"))

''' src: https://stackoverflow.com/questions/53243661/how-to-use-ajax-in-flask-to-iterate-through-a-list '''
@app.route('/get_next', methods=['GET'])
def get_next():
   _direction = request.args.get('direction')
   session['count'] = session['count'] + (1 if _direction == 'f' else - 1)
   _cards = db.session.query(Card).filter_by(created_by = session['deck_r'])

   return jsonify({'card_front':_cards[session['count']].front, 'card_back':_cards[session['count']].back, 'forward':str(session['count']+1 < _cards.count()), 'back':str(bool(session['count']))})

@app.route("/createCard", methods=["POST", "GET"])
@login_required
def createCard():
    form = CreateCard()
    if form.validate_on_submit():
        new_card = Card(deck_name = form.deck_name.data, front = form.front.data, back = form.back.data, created_by=form.deck_name.data)
        deck_ref = Deck.query.filter_by(name = new_card.deck_name).first()
        if (deck_ref is None):
            flash("Please assert that the deck exists.")
            return redirect(url_for("createCard", form = form))
        elif (Card.query.filter_by(deck_name = new_card.deck_name, front = new_card.front).first()):
            flash("You already have a Card with this label")
            return redirect(url_for("createCard", form = form))
        db.session.add(new_card)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("Please assert that all fields are filled.")
            return redirect(url_for("createCard", form = form))
        finally:
            db.session.close()
        return redirect(url_for('decks'))
    return render_template("createCard.html", form = form)

@app.route("/createDeck", methods=["POST", "GET"])
@login_required
def createDeck():
    form = CreateDeck()
    if form.validate_on_submit():
        new_deck = Deck(name = form.name.data, summary = form.summary.data, created_by=current_user.id)
        db.session.add(new_deck)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("This Deck already exists in the system! Please create another instead.")
            return redirect(url_for("createDeck", form = form))
        finally:
            db.session.close()
        return redirect(url_for('decks'))
    return render_template("createDeck.html", form = form)