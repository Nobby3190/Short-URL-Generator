import base64
import hashlib
import re
import threading
from urllib.parse import urlparse

from db.db import DB
from db.models import UrlModel


lock = threading.Lock()


# 檢查網址格式不為空
def validate_url(func: callable) -> callable:
    def wrapper(url: UrlModel):
        if not url:
            print("URL is empty")
            return None
        if isinstance(url, str):
            if not url.strip():
                print("URL is only whitespace")
                return None
            try:
                res = urlparse(url)
                print(f"Parsed URL: {res}")
                if not all([res.scheme, res.netloc]):
                    print("URL missing scheme or netloc")
                    return None
            except ValueError:
                print("ValueError while parsing URL")
                return None

        return func(url)

    return wrapper


# 檢查短網址格式不為空跟其他符號
def validate_hashed_url(func: callable) -> callable:
    def wrapper(hashed_url: str):
        pattern = re.compile(r"^[a-zA-Z0-9]+$")
        if not hashed_url:
            print("URL is empty")
            return "Invalid"
        if isinstance(hashed_url, str):
            if not hashed_url.strip():
                print("URL includes whitespace")
                return "Invalid"
        if not bool(pattern.match(hashed_url)):
            print("URL includes symbols")
            return "Invalid"

        return func(hashed_url)

    return wrapper


# 生成短網址
@validate_url
def hashing_original_url(url: UrlModel) -> str | None:
    """
    1. Hashing the Original URL using SHA-256:
    Use Python's built-in hashlib module to hash the original URL using SHA-256.
    2. Storing the Shortened URL in PostgreSQL:
    Create a table in PostgreSQL to store the mapping between the original URL and the shortened URL.
    3. Storing the Shortened URL in Redis:
    Use Redis to store the mapping between the hash of the original URL and the shortened URL.

    Args:
        url (UrlModel): Original URL

    Returns:
        str: Hashed URL
    """

    # 縮短網址
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()
    short_code = hash_hex[:8]
    hashed = base64.urlsafe_b64encode(short_code.encode()).decode()
    hashed_url = re.sub(r"[^a-zA-Z0-9]", "", hashed)

    db = DB()
    redis = db.r

    # 檢查redis存不存在
    if redis.exists(hashed_url):
        return hashed_url
    # 檢查postgresql存不存在
    postgres = db.p
    with postgres:
        with postgres.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM short_urls WHERE hashed_url = %s", (hashed_url,)
            )
            if cursor.fetchone():
                return hashed_url

            # 不存在寫入postgresql
            cursor.execute(
                "INSERT INTO short_urls (url, hashed_url) VALUES (%s, %s)",
                (url, hashed_url),
            )
            db.p.commit()

    # 不存在寫入redis
    redis.set(hashed_url, url)
    return hashed_url


# 取得原始網址
@validate_hashed_url
def retrieve_url_by_hashed_url(hashed_url: UrlModel) -> str | None:
    """
    When a client inputs a hashed URL, the redirection to the original URL first searches in Redis using the hashed key;
    if not found, it then searches in PostgreSQL.

    Args:
        hashed_url (UrlModel): Input Hashed URL

    Returns:
        str | None: Original URL or None
    """

    db = DB()
    redis = db.r
    postgres = db.p
    # redis裡有資料從redis拿
    if redis.exists(hashed_url):
        url = redis.get(hashed_url)
        url = url.decode("utf-8")
        return url
    else:
        # redis沒有資料從postgresql拿
        with lock:
            with postgres:
                with postgres.cursor() as cursor:
                    cursor.execute(
                        "SELECT url FROM short_urls WHERE hashed_url = %s;",
                        (hashed_url,),
                    )
                    url_row = cursor.fetchone()
                    # 重新寫入redis
                    if url_row:
                        url = url_row[0]
                        redis.set(hashed_url, url)
                        return url
                    else:
                        return None
