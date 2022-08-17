import bcrypt
from flask_app import app
from flask import render_template, redirect, request, flash, session, url_for
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Importing Models
import flask_app.models.user as user

from flask_app.tools import check_email_format


@app.route("/")
def authentication():
    if not session.get("user_id"):
        return render_template("authentication.html")
    return redirect("catalog")


@app.route("/login", methods=["POST", "GET"])
def login():
    if not session.get("user_id"):
        user_ = user.User.get_by_email(request.form)

        if user_:
            match = bcrypt.check_password_hash(user_.password, request.form["password"])

            # Getting User ID in session
            if match:
                session["user_id"] = user_.id
                session["first_name"] = user_.first_name
                session["last_name"] = user_.last_name

            else:
                flash("Incorrect password", "login")
        else:
            flash("Email doesn't exist", "login")

    return redirect(url_for("catalog"))


@app.route("/register", methods=["POST", "GET"])
def register():
    invalid = False
    if not session.get("user_id"):
        if request.method == "POST":
            # Getting form Data
            data = {**request.form}

            if len(data["first_name"]) < 2 or len(data["last_name"]) < 2:
                flash(
                    "First name and last name must contain at least 2 characters",
                    "register",
                )
                invalid = True

            if not check_email_format(data["email"]):
                flash("Email address not valid", "register")
                invalid = True

            if len(data["password"]) < 8:
                flash("Password requires at least 8 characters", "register")
                invalid = True
            else:
                if data["password"] != data["confirm_password"]:
                    flash("Passwords must be the same", "register")
                    invalid = True

            if not invalid:
                # Hashing Password
                data["password"] = bcrypt.generate_password_hash(data["password"])
                user_id = user.User.create(data)

                if user_id:
                    user_ = user.User.get_by_id({"id": user_id})
                    session["user_id"] = user_id
                    session["first_name"] = user_.first_name
                    session["last_name"] = user_.last_name
                    return redirect("/catalog")

                flash("Email already Exists", "register")

    # I used render_template to re-fill fields after fail
    return render_template("authentication.html", register_data=request.form)


@app.route("/logout", methods=["GET"])
def logout():
    if session.get("user_id"):
        del session["user_id"]
        del session["first_name"]
        del session["last_name"]

    return redirect("/")
