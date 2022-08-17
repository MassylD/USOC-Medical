from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL


class Catalog:
    db = "usoc"
    table_name = "catalog"

    def __init__(self, data) -> None:
        self.id = data["id"]

        self.brand = data["brand"]
        self.model = data["model"]
        self.software = data["software"]
        self.option = data["option"]

    # CRUD ----
    @classmethod
    def create(cls, data):
        query = f"INSERT INTO {cls.table_name} (brand, model, software, option) VALUES (%(brand)s, %(model)s, %(software)s, %(option)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def edit(cls, data):
        query = f"UPDATE {cls.table_name} SET brand=%(brand)s, \
                                              model=%(model)s, \
                                              software=%(software)s, \
                                              option=%(option)s \
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
        query = f"SELECT * FROM {cls.table_name} WHERE id=%(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0] if results else None

    @classmethod
    def get_by_id(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0] if results else None

    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM {cls.table_name}"
        data = connectToMySQL(cls.db).query_db(query)
        data_list = []
        if data:
            for d in data:
                data_list.append(cls(d))

        return data_list
