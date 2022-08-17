from curses.ascii import isdigit
from flask_app import app
from flask import render_template, redirect, request, flash, abort, session

from datetime import datetime
from flask_app.tools import check_card_number, check_card_expiry_date

# Importing Models
from flask_app.models.user import User
from flask_app.models.cart import Cart
from flask_app.models.cart_catalog import CartCatalog


@app.route("/cart")
def cart():
    session_id = session.get("user_id")
    if session_id:
        cart = Cart.get({"user_id": session_id})

        if not cart:
            cart = Cart.create({"user_id": session_id})

        cart_catalog = CartCatalog.get_by_cart({"id_cart": cart.id})
        items_count = Cart.items_number({"id_cart": cart.id})
        return render_template(
            "cart.html",
            user_info=session,
            cart=cart,
            cart_catalog=cart_catalog,
            items_count=items_count,
        )
    return redirect("/")


@app.route("/cart-history")
def cart_history():
    session_id = session.get("user_id")
    if session_id:
        cart = Cart.get({"user_id": session_id})

        if not cart:
            cart = Cart.create({"user_id": session_id})

        items_count = Cart.items_number({"id_cart": cart.id})

        cart_history = Cart.get_history({"user_id": session_id})
        return render_template(
            "cart_history.html",
            user_info=session,
            cart_history=cart_history,
            items_count=items_count,
        )
    return redirect("/")


@app.route("/cart/<id>/delete")
def delete_item_from_cart(id):
    session_id = session.get("user_id")
    if session.get("user_id"):
        cart = Cart.get({"user_id": session_id})
        if cart:
            if cart.user.id == session_id:
                CartCatalog.delete({"id_cart": cart.id, "id_catalog": id})
                return redirect("/cart")
            abort(403)
        abort(404)
    return redirect("/")


@app.route("/checkout/<id>", methods=["GET", "POST"])
def checkout(id):
    session_id = session.get("user_id")
    if session.get("user_id"):
        cart = Cart.get_by_id({"id": id})
        if cart:
            if cart.user.id == session_id and not cart.date_checkout:
                if request.method == "POST":
                    invalid = False

                    data = request.form

                    if not data["card_number"]:
                        flash("Card Number is Required", "checkout")
                        invalid = True
                    elif len(data["card_number"]) != 19 or not check_card_number(
                        data["card_number"]
                    ):
                        flash(
                            "Card Number format should be XXXX-XXXX-XXXX-XXXX",
                            "checkout",
                        )
                        invalid = True

                    if not data["expiration_date"]:
                        flash("Expiration Date is Required", "checkout")
                        invalid = True
                    elif len(
                        data["expiration_date"]
                    ) != 5 or not check_card_expiry_date(data["expiration_date"]):
                        flash(
                            "Expiry Date should be MM/YY",
                            "checkout",
                        )
                        invalid = True

                    if not data["security_code"]:
                        flash("Security Code is Required", "checkout")
                        invalid = True
                    elif not data["security_code"].isdigit():
                        flash("Security Code must be a number", "checkout")
                        invalid = True

                    if not invalid:
                        Cart.checkout(
                            {
                                "id": id,
                                "card_number": data.get("card_number"),
                                "security_code": data.get("security_code"),
                                "expiration_date": data.get("expiration_date"),
                            }
                        )
                        return redirect("/catalog")
                items_count = Cart.items_number({"id_cart": cart.id})
                return render_template(
                    "checkout.html",
                    user_info=session,
                    cart=cart,
                    items_count=items_count,
                )
            abort(403)
        abort(404)
    return redirect("/")
