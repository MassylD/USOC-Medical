from flask_app.models import cart, catalog
from flask_app.config.mysqlconnection import connectToMySQL


class CartCatalog:
    db = "usoc"
    table_name = "cart_catalog"

    def __init__(self, data) -> None:
        self.cart = cart.Cart.get_by_id({"id": data["fk_cart"]})
        self.catalog = catalog.Catalog.get_by_id({"id": data["fk_catalog"]})

    # CRUD ----
    @classmethod
    def create(cls, data):
        query = f"INSERT INTO {cls.table_name} VALUES (%(fk_cart)s, %(fk_catalog)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def edit(cls, data):
        query = f"UPDATE {cls.table_name} SET fk_cart=%(fk_cart)s, \
                                              fk_catalog=%(fk_catalog)s, \
                                              WHERE fk_cart=%(id_cart)s and fk_catalog=%(id_catalog)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0] if results else None

    @classmethod
    def delete(cls, data):
        query = f"DELETE FROM {cls.table_name} WHERE fk_cart=%(id_cart)s and fk_catalog=%(id_catalog)s"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def get_by_cart(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE fk_cart=%(id_cart)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        data_list = []
        if results:
            for data in results:
                data_list.append(cls(data))
        return data_list


    @classmethod
    def check_catalog_exists_by_cart(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE fk_cart=%(id_cart)s and fk_catalog=%(id_catalog)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0] if results else None


    @classmethod
    def get_item_number_by_cart(cls, data):
        query = (
            f"SELECT COUNT(*) AS COUNT FROM {cls.table_name} WHERE fk_cart=%(id_cart)s"
        )
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0].get("COUNT") if results else None
