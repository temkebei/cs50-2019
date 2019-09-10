import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
application = app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.getenv("secret")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET"])
@login_required
def index():
    total = 0
    data = []
    user_id = session["user_id"]
    cash = db.execute("SELECT cash from users where id = :id", id=user_id)[0]['cash']
    select_user = db.execute(
        'SELECT "symbol",SUM("share") as sum FROM "transactions" WHERE "user_id" = :user_id GROUP BY "symbol"', user_id=user_id)

    if len(select_user) > 0:
        for i in select_user:
            if i['sum'] > 0:
                quote = lookup(i['symbol'])
                temp = {
                    'symbol': quote['symbol'],
                    'name': quote['name'],
                    'shares': i['sum'],
                    'price': usd(quote['price']),
                    'total': i['sum']*quote['price']
                }
                total += temp['total']
                temp['total'] = usd(temp['total'])
                data.append(temp)

        return render_template("index.html", data=data, total=usd(total+cash), cash=usd(cash))
    return render_template("index.html", total=cash, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure password was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("Invalid symbol", 400)

        cash = db.execute("SELECT cash from users where id = :id", id=session["user_id"])[0]['cash']

        if (float(request.form.get("shares")) * quote['price'] > cash):
            return apology("CANT AFFORD, you are poor", 400)

        db.execute("INSERT into transactions (user_id,company,price,share,symbol,cost) values ( :user_id , :company , :price , :share,:symbol,:cost)",
                   user_id=session["user_id"], company=quote['name'], price=quote['price'], share=float(request.form.get("shares")), symbol=quote["symbol"],
                   cost=float(request.form.get("shares")) * quote['price'])

        db.execute("UPDATE users SET cash = :rem_cash WHERE id = :id ", rem_cash=cash - (float(request.form.get("shares")) * quote['price']),
                   id=session["user_id"])

        flash('Bought!')
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    history = db.execute("SELECT symbol,share,price,timestamp,action FROM transactions where user_id = :user_id",
                         user_id=session["user_id"])

    return render_template("history.html", data=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("Must give symbol", 400)

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Invalid symbol", 400)
        quote['price'] = usd(quote['price'])
        return render_template("quote.html",
                               quote=quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if(len(rows) > 0):
            flash('User already exists! Try a different user name.')
            return render_template("register.html")

        db.execute("INSERT into users ( username,hash) values (:username,:hash)",
                   username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
        return render_template("login.html")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    user_id = session["user_id"]
    select_user = db.execute(
        'SELECT "symbol",SUM("share") as sum FROM "transactions" WHERE "user_id" = :user_id   GROUP BY "symbol"', user_id=user_id)

    symbols = []

    for x in select_user:
        if x['sum'] > 0:
            symbols.append(x['symbol'])

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        num_shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")

        for x in select_user:
            if x['symbol'] == symbol:
                if x['sum'] < num_shares:
                    return apology("Not enough shares", 400)

                quote = lookup(symbol)

                price_curr = quote['price']*float(num_shares)

                db.execute("INSERT into transactions (user_id,company,price,share,symbol,cost,action) values ( :user_id , :company , :price , :share,:symbol,:cost,:action)",
                           user_id=user_id, company=quote['name'], price=quote['price'],share=int(num_shares)*-1, symbol=quote["symbol"],
                           cost=price_curr, action='s')

                db.execute("UPDATE users SET cash = cash + :price_curr WHERE id = :id ", price_curr=price_curr,
                          id=user_id)

                flash('Sold!')
                return redirect("/")

    return render_template("sell.html", symbols=symbols)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        if not request.form.get("addfunds"):
            return apology("please enter amount you would like to add")
        add = float(request.form.get("addfunds"))
        db.execute("UPDATE users SET cash=cash+:add WHERE id=:userId;", add=add, userId=session["user_id"])
        return redirect("/")
    else:
        return render_template("add.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run()
