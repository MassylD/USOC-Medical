from asyncio.log import logger
import pymysql.cursors


class MySqlConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="DeeDeene1992",
            db=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit
                    return cursor.lastrowid
                return cursor.fetchall()
            except Exception as e:
                print(e)
                return False
            finally:
                self.connection.close()


def connectToMySQL(db):
    return MySqlConnection(db)
