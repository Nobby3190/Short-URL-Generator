import base64
import hashlib
import re

from db.db import DB
from db.models import UrlModel


def hash_url(url: UrlModel) -> str:
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()
    short_code = hash_hex[:8]
    hashed = base64.urlsafe_b64encode(short_code.encode()).decode()
    hashed = re.sub(r"[^a-zA-Z0-9]", "", hashed)

    if "https://" in url.input_url:
        hashed_url = "https://" + hashed + ".com"
    elif "http://" in url.input_url:
        hashed_url = "http://" + hashed + ".com"

    # store in postgresql
    db = DB()
    postgres = db.p
    with postgres:
        with postgres.cursor():
            postgres.cursor().execute(
                "INSERT INTO short_urls (url, hashed_url) VALUES (%s, %s)",
                (url, hashed_url),
            )
            db.p.commit()

    # store in redis
    redis = db.r
    redis.set(hashed_url, url)

    return hashed_url


def retrieve_url_by_hashed_url(hashed_url: UrlModel) -> str | None:
    db = DB()
    redis = db.r
    postgres = db.p
    if redis.exists(hashed_url.hashed_url):
        url = redis.get(hashed_url.hashed_url)
        url = url.decode("utf-8")
        return url
    else:
        with postgres:
            with postgres.cursor() as cursor:
                cursor.execute(
                    "SELECT url FROM short_urls WHERE hashed_url = %s;",
                    (hashed_url.hashed_url,),
                )
                url_row = cursor.fetchone()
                if url_row:
                    url = url_row[0]
                    redis.set(hashed_url.hashed_url, url)
                    return url
                else:
                    return None
