from fastapi import APIRouter, status, HTTPException, Depends
from models import UserIn, UserOut
from Database import get_db
from hashing import Hash

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