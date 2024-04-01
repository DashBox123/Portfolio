import os
from datetime import date, datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Getting user
    user_id = session["user_id"]
    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", user_id
    )[0]["cash"]

    # Updating stock prices in database for current user
    # Returns list of dictionaries containing distinct symbols that the user has invested in
    symbols_dict = db.execute(
        "SELECT DISTINCT stock_symbol FROM portfolio WHERE user_id = ?", user_id
    )
    # if the portfolio is empty i.e. user owns 0 stocks
    if not symbols_dict:
        return render_template("index.html", cash=cash, spent=0, total=cash, stock_assets=0)

    # if the user owns 0 of any stock
    db.execute(
        "DELETE FROM portfolio WHERE user_id = ? AND stock_quantity = ?", user_id, 0
    )

    # Extract symbols from dictionaries into a single list
    symbols = [value for d in symbols_dict for value in d.values()]

    # Update database with current stock prices
    for symbol in symbols:
        db.execute(
            "UPDATE portfolio SET stock_price = ? WHERE user_id = ? AND stock_symbol = ?", lookup(symbol)[
                "price"], user_id, symbol
        )
    # Gets updated data for user
    portfolio = db.execute(
        "SELECT stock_symbol, purchase_price, stock_price, SUM(stock_quantity) AS stock_quantity FROM portfolio WHERE user_id = ? GROUP BY stock_symbol", user_id
    )
    # Calculates total stock assets for user
    stock_assets = db.execute(
        "SELECT SUM(stock_quantity * stock_price) AS stock_assets FROM portfolio WHERE user_id = ?", user_id
    )[0]["stock_assets"]
    # if the user has no stock assets set to 0
    if not stock_assets:
        stock_assets = 0
    # Calculates total user has spent
    spent = db.execute(
        "SELECT SUM(stock_quantity * purchase_price) AS spent FROM portfolio WHERE user_id = ?", user_id
    )[0]["spent"]

    return render_template("index.html", portfolio=portfolio, cash=cash, spent=spent, total=stock_assets + cash, stock_assets=stock_assets)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # When user loads page
    if request.method == "GET":
        return render_template("buy.html")

    # If request is POST i.e. user has entered some values
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")
    if not symbol:
        return apology("Missing Stock Symbol")
    if lookup(symbol) is None:
        return apology("Invalid Symbol")
    if not shares:
        return apology("Missing Share Quantity")
    try:
        val = int(shares)
    except ValueError:
        return apology("Invalid Share Quantity",400)
    if not int(shares) > 0:
        return apology("Invalid Share Quantity",400)

    stock_price = lookup(symbol)["price"]
    shares = int(shares)
    cost = stock_price * shares
    # Check how much money the user currently has
    # Current user logged in
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"]
    )[0]
    if cost > user["cash"]:
        return apology("Insufficient Funds")

    # Adding purchase to portfolio database
    # Checking if user already owns this stock
    stocks_owned_dict = db.execute(
        "SELECT DISTINCT stock_symbol FROM portfolio WHERE user_id = ?", user["id"]
    )
    stocks_owned = [value for d in stocks_owned_dict for value in d.values()]
    if symbol in stocks_owned:
        db.execute(
            "UPDATE portfolio SET stock_quantity = stock_quantity + ? WHERE user_id = ? AND stock_symbol = ?", shares, user[
                "id"], symbol
        )
    # if user does not already own these stocks
    else:
        db.execute(
            "INSERT INTO portfolio (user_id,stock_symbol,stock_quantity,purchase_price,stock_price) VALUES (?,?,?,?,?)", user[
                "id"], symbol, shares, stock_price, stock_price
        )

    # Adding purchase to transactions database
    db.execute(
        "INSERT INTO transactions (user_id, stock_symbol, stock_quantity, price, date, time, type) VALUES (?,?,?,?,?,?,?)", user[
            "id"], symbol, shares, stock_price, date.today(), datetime.now().strftime("%H:%M:%S"), "BUY"
    )
    # substracting the purchase amount from user's current cash
    remaining_cash = user["cash"] - cost
    db.execute(
        "UPDATE users SET cash = ? WHERE id = ?", remaining_cash, user["id"]
    )
    # redirect to home page
    return redirect("/")


@app.route("/history")
@login_required
def portfolio():
    """Show portfolio of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", session["user_id"]
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # When user loads page
    if request.method == "GET":
        return render_template("quote.html")

    # When user submits symbol for quote
    quote = lookup(request.form.get("symbol"))
    if quote is None:
        return apology("Stock Symbol invalid", 400)
    # If quote is legit show user quote price
    return render_template("quoted.html", quote=quote, quote_price=usd(quote["price"])), 200


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # user has filled in and entered the registration form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # validating that user has filled in username field
        if not username:
            return apology("must provide username", 400)

        # checking if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("Username already exists", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # TODO: Ensure user entered password is strong enough
        # Ensure user password is at least 10 characters


        # Ensure confirmation was submitted
        elif not confirmation:
            return apology("must re-enter password")

        # Ensure passwords match
        elif not password == confirmation:
            return apology("Passwords do not match")

        # Enter user's details into sql database
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                                 username, generate_password_hash(password))

        # Log the user in automatically
        session["user_id"] = new_user_id

        # Take user to their home page once logged in
        return redirect("/"), 200

    if request.method == "GET":
        # user has simply clicked on the register page and should be displayed
        # the register page only
        return render_template("register.html"), 200


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Getting user
    user_id = session["user_id"]
    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", user_id
    )[0]["cash"]

    # Obtaining list of symbols user has invested in
    symbols_dict = db.execute(
        "SELECT DISTINCT stock_symbol FROM portfolio WHERE user_id = ?", user_id
    )
    symbols = [value for d in symbols_dict for value in d.values()]

    # if GET
    if request.method == "GET":
        return render_template("sell.html", symbols=symbols)

    # if POST
    # input validation
    # ensure user has selected a symbol
    symbol = request.form.get("symbol")
    if not symbol:
        return apology("Missing Stock Symbol")

    # ensure user has selected valid share quantity
    shares = request.form.get("shares")
    if not shares:
        return apology("Missing Share Count")
    try:
        shares = int(shares)
    except ValueError:
        return apology("Invalid Share Quantity")
    shares_held = db.execute(
        "SELECT SUM(stock_quantity) AS stock_quantity FROM portfolio WHERE user_id = ? AND stock_symbol = ?", user_id, symbol
    )[0]["stock_quantity"]
    if shares > shares_held:
        return apology("You do not own enough shares")

    # updating portfolio
    db.execute(
        "UPDATE portfolio SET stock_quantity = stock_quantity - ? WHERE user_id = ? AND stock_symbol = ?", shares, user_id, symbol
    )

    # Adding sale to transactions database
    db.execute(
        "INSERT INTO transactions (user_id, stock_symbol, stock_quantity, price, date, time, type) VALUES (?,?,?,?,?,?,?)", user_id, symbol, shares, lookup(
            symbol)["price"], date.today(), datetime.now().strftime("%H:%M:%S"), "SELL"
    )

    # Adding the sale amount to user's current cash
    cash = cash + (shares*lookup(symbol)["price"])
    db.execute(
        "UPDATE users SET cash = ? WHERE id = ?", cash, user_id
    )
    # redirect to home page
    return redirect("/")
