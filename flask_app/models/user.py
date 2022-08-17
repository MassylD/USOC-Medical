from flask_app.config.mysqlconnection import connectToMySQL


class User:
    db = "usoc"
    table_name = "USER"

    def __init__(self, data) -> None:
        self.id = data["id"]
        self.email = data["email"]
        self.password = data["password"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # CRUD ----
    @classmethod
    def create(cls, data):
        print(data)
        query = f"INSERT INTO {cls.table_name} (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_by_email(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE email=%(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else False

    @classmethod
    def get_by_id(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else False
