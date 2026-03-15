from fastapi import APIRouter, status, HTTPException, Depends
from models import UserIn, UserOut
from Database import get_db
from datetime import datetime as dt, timedelta, timezone
from jose import jwt
import os
from dotenv import load_dotenv
from hashing import Hash

secret_key = load_dotenv()

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def add_admin(new_user: UserIn, db = Depends(get_db)):

    hashed_pass = Hash.bcrypt(new_user.password)

    cursor = db.cursor()
    new_id = cursor.var(int)

    cursor.callproc('p_add_admin', [new_user.user_name, hashed_pass, new_id])

    result = {

        'message': f'{new_id.getvalue()} credentials saved!!'
    }
    return result


def generate_token(data: dict): # Create to generate (Json Web Tokens) when a user logged in

    to_encode = data.copy()

    exp_time = dt.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({'exp': exp_time})

    encode_jwt = jwt.encode(to_encode, algorithm='HS256', key=os.environ.get('SECRET_KEY'))

    return encode_jwt
