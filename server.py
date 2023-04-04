from flask import (Flask, render_template, request, flash, session,redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():

    return render_template ('homepage.html')


@app.route('/login')
def login():

    return render_template('login.html')

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Please try again with another email.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/login")

@app.route('/todos',methods=["POST"])
def todo_detail():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/login')
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return render_template("todo_details.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
