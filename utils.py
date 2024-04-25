import base64
import hashlib
import re

from db.db import DB
from db.models import UrlModel


def hash_url(url: UrlModel) -> str:
    """
    1. Hashing the Original URL using SHA-256:
    You can use Python's built-in hashlib module to hash the original URL using SHA-256.
    2. Storing the Shortened URL in PostgreSQL:
    You can create a table in PostgreSQL to store the mapping between the original URL and the shortened URL.
    3. Storing the Shortened URL in Redis:
    You can use Redis to store the mapping between the hash of the original URL and the shortened URL.

    Args:
        url (UrlModel): Original URL

    Returns:
        str: Hashed URL
    """

    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()
    short_code = hash_hex[:8]
    hashed = base64.urlsafe_b64encode(short_code.encode()).decode()
    hashed = re.sub(r"[^a-zA-Z0-9]", "", hashed)

    if "https://" in url:
        hashed_url = "https://" + hashed + ".com"
    elif "http://" in url.url:
        hashed_url = "http://" + hashed + ".com"

    db = DB()
    postgres = db.p
    with postgres:
        with postgres.cursor():
            postgres.cursor().execute(
                "INSERT INTO short_urls (url, hashed_url) VALUES (%s, %s)",
                (url, hashed_url),
            )
            db.p.commit()

    redis = db.r
    redis.set(hashed_url, url)

    return hashed_url


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
    if redis.exists(hashed_url):
        url = redis.get(hashed_url)
        url = url.decode("utf-8")
        return url
    else:
        with postgres:
            with postgres.cursor() as cursor:
                cursor.execute(
                    "SELECT url FROM short_urls WHERE hashed_url = %s;",
                    (hashed_url,),
                )
                url_row = cursor.fetchone()
                if url_row:
                    url = url_row[0]
                    redis.set(hashed_url, url)
                    return url
                else:
                    return None
