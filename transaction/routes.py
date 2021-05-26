from flask import render_template, url_for, redirect, request, flash
from flask_wtf import form
from transaction import app, db, bcrypt
from transaction.forms import ChangePassword, RegistrationForm, LoginForm
from transaction.models import User, Transaction
from pytz import timezone
from sqlalchemy import or_
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        name = request.form['name']
        card_number = request.form['cardnumber']
        card_type = request.form['cardtype']
        amount_withdrawal = request.form['withdrawal']
        amount_remaining = request.form['remaining']
        wallet_balance = request.form['walletbalance']
        transaction_date = datetime.now(
            timezone("Asia/Kolkata")).replace(microsecond=0)

        new_transaction = Transaction(name=name, card_number=card_number, card_type=card_type,
                                      amount_withdrawal=amount_withdrawal, amount_remaining=amount_remaining,
                                      wallet_balance=wallet_balance, transaction_date=transaction_date, user_id=current_user.id)

        try:
            db.session.add(new_transaction)
            db.session.commit()
            return redirect('/home')
        except:
            return "There was issue in adding your Transaction"

    else:
        transaction = Transaction.query.filter_by(user_id=current_user.id).order_by(
            Transaction.transaction_date.desc()).all()
        return render_template('home.html', transactions=transaction)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    transaction = Transaction.query.get(id)

    if request.method == 'POST':
        transaction.name = request.form['name']
        transaction.card_number = request.form['cardnumber']
        transaction.card_type = request.form['cardtype']
        transaction.amount_withdrawal = request.form['withdrawal']
        transaction.amount_remaining = request.form['remaining']
        transaction.wallet_balance = request.form['walletbalance']
        transaction.transaction_date = datetime.now(
            timezone("Asia/Kolkata")).replace(microsecond=0)
        try:
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'There was issue in updating your transaction'
    else:
        return render_template('update.html', transaction=transaction)


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if request.method == 'POST':
        search = request.form['search']
        search = "%{}%".format(search)
        results = Transaction.query.filter(or_(Transaction.transaction_date.like(search),
                                               Transaction.name.like(search), Transaction.card_number.like(
                                                   search), Transaction.card_type.like(search),
                                               Transaction.amount_withdrawal.like(
                                                   search), Transaction.amount_remaining.like(search),
                                               Transaction.wallet_balance.like(search))).all()
        if results:
            return render_template('search.html', transactions=results)

    return redirect(url_for('home'))


@app.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add(id):
    transaction = Transaction.query.get(id)

    if request.method == 'POST':
        name = request.form['name']
        card_number = request.form['cardnumber']
        card_type = request.form['cardtype']
        amount_withdrawal = request.form['withdrawal']
        amount_remaining = request.form['remaining']
        wallet_balance = request.form['walletbalance']
        transaction_date = datetime.now(
            timezone("Asia/Kolkata")).replace(microsecond=0)

        new_transaction = Transaction(name=name, card_number=card_number, card_type=card_type,
                                      amount_withdrawal=amount_withdrawal, amount_remaining=amount_remaining, wallet_balance=wallet_balance, transaction_date=transaction_date)

        try:
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return "There was issue in adding your Transaction"

    else:
        return render_template('/add.html', transaction=transaction)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data,
                    username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can  log in', "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Pleas check mail and password")

    return render_template('login.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # if current_user.is_authenticated:
    # 	return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        userlist = User.query.all()
        user = User.query.filter_by(email="jaffarjawed@gmail.com").first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('userlist'))
        else:
            flash("Login Unsuccessful. Pleas check mail and password")
    
    return render_template('admin.html', form=form)


@app.route('/userlist', methods=['GET', 'POST'])
@login_required
def userlist():

    userlist = User.query.all()
    return render_template('userlist.html', userlist=userlist)


@app.route('/viewuser/<int:id>')
@login_required
def viewuser(id):
    transaction = Transaction.query.filter_by(user_id=id).order_by(
        Transaction.transaction_date.desc()).all()
    if transaction:
        return render_template('view.html', transactions=transaction)
    else:
        flash("Transaction does not exist for this user")
    return render_template('view.html', transactions=transaction)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')



@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    user = User.query.get(current_user.id)
    form = ChangePassword()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user.password = hashed_password
            try:
                db.session.commit()
                flash("You have successfully updated your password")
                return redirect(url_for('logout'))
            except:
                return 'There was issue in changing your password'

    return render_template('changepassword.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
