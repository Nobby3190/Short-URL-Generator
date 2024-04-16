import psycopg2
import redis
import redis.exceptions


class DB:
    def __init__(self) -> None:
        self.r = redis.Redis(
            host="localhost", port=6379, username="default", password="123456", db=0
        )
        self.p = psycopg2.connect(
            dbname="url",
            host="localhost",
            port=5432,
            user="nobby",
            password="nobby",
            sslmode="allow",
        )

    def check_redis_connect(self) -> None:
        try:
            print(self.r.ping())
        except (Exception, redis.exceptions) as error:
            print(f"Error connecting to redis: {error}")

    def check_postgres_connect(self) -> None:
        try:
            cursor = self.p.cursor()
        except (Exception, psycopg2.Error) as error:
            print(f"Error connecting to postgresql: {error}")
        finally:
            if self.p:
                cursor.close()
                self.p.close()
                print("PostgreSQL connection closed")

    def select_postgres_tables(self):
        cursor = self.p.cursor()
        with self.p:
            with cursor:
                cursor.execute(
                    "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"
                )
                rows = cursor.fetchall()
                table_names = [row[0] for row in rows]

                # 打印所有表名
                for table_name in table_names:
                    print(table_name)


#     def select_postgres_table(self):
#         cursor = self.p.cursor()
#         with self.p:
#             with cursor:
#                 cursor.execute("SELECT * FROM short_urls;")
#                 result = cursor.fetchall()
#                 print(result)


#     def get_redis_value(self):
#         retrieved_url = self.r.get("https://MDZjNjA0MzY.com")
#         print("Retrieved URL:", retrieved_url)


# if __name__ == "__main__":
#     db = DB()
#     db.get_redis_value()
