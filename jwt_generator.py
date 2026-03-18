from datetime import datetime as dt, timedelta, timezone
from jose import jwt
import os

def generate_token(data: dict): # Create to generate (Json Web Tokens) when a user logged in

    to_encode = data.copy()

    exp_time = dt.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({'exp': exp_time})

    encode_jwt = jwt.encode(to_encode, algorithm='HS256', key=os.environ.get('SECRET_KEY'))

    return encode_jwt
