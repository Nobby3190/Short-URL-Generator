import base64
import hashlib
import re

from db.db import DB


def generate_short_url(url: str) -> str:
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()

    short_code = hash_hex[:8]
    hashed = base64.urlsafe_b64encode(short_code.encode()).decode()
    hashed = re.sub(r"[^a-zA-Z0-9]", "", hashed)

    if "https://" in url:
        hashed_url = "https://" + hashed + ".com"
    elif "http://" in url:
        hashed_url = "http://" + hashed + ".com"

    data = {"url": url, "hashed_url": hashed_url}

    # store in postgresql
    db = DB()
    postgres = db.p
    cursor = postgres.cursor()
    query = """INSERT INTO short_urls (url, hashed_url) VALUES (%s, %s)"""
    with postgres:
        with cursor:
            cursor.execute(query, (url, hashed_url))
            db.p.commit()

    # store in redis
    redis = db.r
    redis.set(data["hashed_url"], data["url"])

    return hashed_url
