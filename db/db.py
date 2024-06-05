import psycopg2
import redis
import redis.exceptions


class DB:
    def __init__(self) -> None:
        self.r = redis.Redis(
            host="redis", port=6379, username="default", password="123456", db=0
        )
        self.p = psycopg2.connect(
            dbname="postgres",
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
                            url VARCHAR(155) NOT NULL,
                            hashed_url VARCHAR(50) UNIQUE NOT NULL
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
