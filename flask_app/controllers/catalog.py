from flask_app import app
from flask import render_template, redirect, request, flash, abort, session

from datetime import datetime

# Importing Models
from flask_app.models.catalog import Catalog
from flask_app.models.cart import Cart
from flask_app.models.user import User


@app.route("/catalog")
def catalog():
    session_id = session.get("user_id")
    if session.get("user_id"):
        user_ = User.get_by_id({"id": session["user_id"]})
        catalog = Catalog.get_all()

        for c in catalog:
            exists = Cart.check_in_cart({"user_id": session_id, "id_item": c.id})
            c.exists = exists

        cart = Cart.get({"user_id": session_id})

        if not cart:
            cart = Cart.create({"user_id": session_id})


        items_count = Cart.items_number({"id_cart": cart.id})

        return render_template(
            "catalog.html", user_info=user_, catalog=catalog, items_count=items_count
        )
    return redirect("/")


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if session.get("user_id"):
        if request.method == "POST":
            invalid = False

            user_id = session.get("user_id")

            data = request.form

            if not invalid:
                Cart.add_to_cart({"id_item": data.get("id_item"), "user_id": user_id})

    return redirect("/catalog")
