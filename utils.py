import base64
import hashlib
import re


def generate_short_url(url: str):
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()
    
    short_code = hash_hex[:8]
    short_url = base64.urlsafe_b64encode(short_code.encode()).decode()
    short_url = re.sub(r'[^a-zA-Z0-9]', '', short_url)
    
    
    
    if "https://" in url:
        short_url = "https://" + short_url + ".com"
    else:
        short_url = "http://" + short_url + ".com"
    return short_url
