from flask_app.models import user, cart_catalog
from flask_app.config.mysqlconnection import connectToMySQL


class Cart:
    db = "usoc"
    table_name = "cart"

    def __init__(self, data) -> None:
        self.id = data["id"]
        self.user = user.User.get_by_id({"id": data["user_id"]})
        self.created = data["created"]

        self.card_number = data["card_number"]
        self.security_code = data["security_code"]
        self.expiration_date = data["expiration_date"]
        self.date_checkout = data["date_checkout"]

    # CRUD ----
    @classmethod
    def create(cls, data):
        query = f"INSERT INTO {cls.table_name} (USER_ID) VALUES (%(user_id)s)"
        result = connectToMySQL(cls.db).query_db(query, data)

        return cls.get_by_id({"id": result})

    @classmethod
    def edit(cls, data):
        query = f"UPDATE {cls.table_name} SET card_number=%(card_number)s, \
                                              security_code=%(security_code)s, \
                                              expiration_date=%(expiration_date)s, \
                                              date_checkout=%(date_checkout)s \
                                              WHERE ID=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0] if results else None

    @classmethod
    def delete(cls, data):
        query = f"DELETE FROM {cls.table_name} WHERE ID=%(id)s"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def get(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE user_id=%(user_id)s and date_checkout IS NULL"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else None

    @classmethod
    def get_by_id(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else None

    @classmethod
    def get_history(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE user_id=%(user_id)s and date_checkout IS NOT NULL"
        data = connectToMySQL(cls.db).query_db(query, data)

        data_list = []
        if data:
            for d in data:
                cart = cls(d)
                cart.items = cart_catalog.CartCatalog.get_by_cart({"id_cart": cart.id})
                cart.items_number = cls.items_number({"id_cart": cart.id})
                data_list.append(cart)

        return data_list

    @classmethod
    def add_to_cart(cls, data):
        user_data = {"user_id": data.get("user_id")}
        cart = cls.get(user_data)

        # Check if a Cart not checked out exists
        if not cart:
            cart = cls.create(user_data)

        cart_catalog.CartCatalog.create(
            {"fk_cart": cart.id, "fk_catalog": int(data.get("id_item"))}
        )

        return

    @classmethod
    def items_number(cls, data):
        return cart_catalog.CartCatalog.get_item_number_by_cart(data)

    @classmethod
    def checkout(cls, data):
        query = f"UPDATE {cls.table_name} SET card_number=%(card_number)s, \
                                              security_code=%(security_code)s, \
                                              expiration_date=%(expiration_date)s, \
                                              date_checkout=NOW() \
                                              WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0] if results else None

    @classmethod
    def check_in_cart(cls, data):
        cart = cls.get({"user_id": data.get("user_id")})
        return (
            True
            if cart
            and cart_catalog.CartCatalog.check_catalog_exists_by_cart(
                {"id_cart": cart.id, "id_catalog": data.get("id_item")}
            )
            else False
        )
