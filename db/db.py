import psycopg2
import redis
import redis.exceptions


class DB:
    def __init__(self) -> None:
        self.r = redis.Redis(
            host="redis", port=6379, username="default", password="123456", db=0
        )
        self.p = psycopg2.connect(
            dbname="urls",
            host="postgres",
            port=5432,
            user="nobby",
            password="nobby",
            sslmode="allow",
        )

        with self.p:
            with self.p.cursor() as cursor:
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS short_urls (
                            url TEXT NOT NULL,
                            hashed_url TEXT UNIQUE NOT NULL
                        );
                        """)
            self.p.commit()

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

    def create_table(self):
        cursor = self.p.cursor()
        with self.p:
            with cursor:
                query = """
                    CREATE TABLE IF NOT EXISTS short_urls (
                        url TEXT NOT NULL,
                        hashed_url TEXT UNIQUE NOT NULL
                    );
                    """

                cursor.execute(query=query)
                self.p.commit()

    #     def select_postgres_tables(self):
    #         cursor = self.p.cursor()
    #         with self.p:
    #             with cursor:
    #                 cursor.execute(
    #                     "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"
    #                 )
    #                 rows = cursor.fetchall()
    #                 table_names = [row[0] for row in rows]

    #                 # 打印所有表名
    #                 for table_name in table_names:
    #                     print(table_name)

    # def select_postgres_table(self):
    #     cursor = self.p.cursor()
    #     with self.p:
    #         with cursor:
    #             cursor.execute(
    #                 "SELECT url FROM short_urls WHERE hashed_url = %s;",
    #                 ("https://ZDBlMTk2YTA.com",),
    #             )
    #             result = cursor.fetchone()
    #             print(result[0])

    def select_postgres_table(self):
        cursor = self.p.cursor()
        with self.p:
            with cursor:
                cursor.execute("SELECT * FROM short_urls;")
                result = cursor.fetchall()
                for row in result:
                    print(row)

    #     def get_redis_value(self, hashed_url):
    #         if self.r.exists(hashed_url):
    #             retrieved_url = self.r.get(hashed_url)
    #             r = retrieved_url.decode("utf-8")
    #             print(r)

    #     def delete_redis_db_data(self):
    #         self.r.flushdb()
    #         print("ok")

    def delete_postgresql_table_data(self):
        query = "DELETE FROM short_urls"
        with self.p as postgres:
            with postgres.cursor() as cursor:
                cursor.execute(query)
                postgres.commit()
        print("ok")
