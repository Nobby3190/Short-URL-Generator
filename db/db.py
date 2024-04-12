import redis
import psycopg2
import redis.exceptions


class DB():
    def __init__(self) -> None:
        self.r = redis.Redis(
                host="localhost", 
                port=6379, 
                username='default', 
                password='123456', 
                db=0
            )
        self.p = psycopg2.connect(
                dbname='url',
                host='localhost',
                port=5432,
                user='nobby',
                password='nobby',
                sslmode='allow'
            )
    
        
    def redis_connect(self) -> None:
        try:
            print(self.r.ping())
        except (Exception, redis.exceptions) as error:
            print(f"Error connecting to redis: {error}")


    def postgres_connect(self) -> None:
        try:
            cursor = self.p.cursor()
        except (Exception, psycopg2.Error) as error:
            print(f"Error connecting to postgresql: {error}")
        finally:
            if self.p:
                cursor.close()
                self.p.close()
                print("PostgreSQL connection closed")
                
                
    def create_postgres_table(self) -> None:
        if self.postgres_connect:
            cursor = self.p.cursor()
            create_table = """
                CREATE TABLE IF NOT EXISTS short_urls (
                    url TEXT NOT NULL,
                    hashed_url TEXT NOT NULL
                );
                """
            cursor.execute(create_table)
            self.p.commit()
            
            cursor.close()
            self.p.close()
            print("ok")
            
    
    
if __name__ == "__main__":
    db = DB()
    db.create_postgres_table()