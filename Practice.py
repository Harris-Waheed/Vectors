from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel
import uvicorn
import oracledb
from Database import get_db

app = FastAPI()


class DonorIn(BaseModel):

    # id will assign automatically by database
    name: str
    age: int
    phone: str
    bg: str


class DonorOut(BaseModel):

    id: int
    name: str
    age: int
    bg: str
    lst_don: str


def pagination(skip: int = 0, limit: int = 2):

    return {'skip': skip, 'limit': limit}


@app.post('/donors/', response_model=DonorOut, status_code=status.HTTP_201_CREATED)
def add_donor(donor_data: DonorIn, db=Depends(get_db)):

    cursor = db.cursor()
    new_id = cursor.var(int)
    new_date = cursor.var(str)

    data = [donor_data.name, donor_data.age, donor_data.phone, donor_data.bg, new_id, new_date]
    cursor.callproc('p_get_donor', data)

    donor_data = {

        'id': new_id.getvalue(),
        'name': donor_data.name,
        'age': donor_data.age,
        'bg': donor_data.bg,
        'lst_don': new_date.getvalue()
    }

    return donor_data


@app.get('/donors/', response_model=list[DonorOut])
def display_donors(pagi: dict = Depends(pagination), db=Depends(get_db)):

    skip = pagi['skip']
    limit = pagi['limit']

    cursor = db.cursor()
    ref_cursor = cursor.var(oracledb.CURSOR)
    cursor.callproc('p_display_donor', [ref_cursor])
    result = ref_cursor.getvalue()

    rows = result.fetchall()

    donors_list = []

    for row in rows:

        donor_dict = {

            'id': row[0],
            "name": row[1],
            'age': row[2],
            'bg': row[3],
            'lst_don': row[4]
        }

        donors_list.append(donor_dict)

    return donors_list[skip: skip + limit]


@app.get('/donor/{donor_id}', response_model=DonorOut)
def display_donor(donor_id: int, db=Depends(get_db)):

    cursor = db.cursor()
    ref_cursor = cursor.var(oracledb.CURSOR)
    cursor.callproc('p_display_donor', [ref_cursor])
    result = ref_cursor.getvalue()

    rows = result.fetchall()

    for row in rows:
        if int(row[0]) == donor_id:
            donor_dict = {

                'id': row[0],
                "name": row[1],
                'age': row[2],
                'bg': row[3],
                'lst_don': row[4]
            }

            return donor_dict

    raise HTTPException(status_code=404, detail='Donor Id Not Found!')


@app.put('/donors/{donor_id}')
def update_donor(donor_id: int, new_phone: str, db=Depends(get_db)):

    cursor = db.cursor()

    new_number = cursor.var(str)

    cursor.callproc('p_update_donor', [donor_id, new_phone, new_number])

    updated_data = {

        'updated_id': donor_id,
        'new_number': new_number.getvalue()
    }

    return updated_data


@app.delete('/donors/{donor_id}')
def delete_donor(donor_id: int, db=Depends(get_db)):

    cur = db.cursor()
    result = cur.var(int)

    cur.callproc('p_delete_donor', [donor_id, result])

    if result.getvalue() == 1:
        message = {'message': f'{donor_id} deleted!'}

        return message

    raise HTTPException(status_code=404, detail='Id not found!')


if __name__ == '__main__':

    uvicorn.run('main2:app', host='localhost', port=8000)

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import oracledb
from Database import get_db  # Assuming your database.py is in the main folder

# 1. We create a router instead of an app
# 2. The prefix="/donors" means we never have to type '/donors' in our routes again!
router = APIRouter(
    prefix="/donors",
    tags=["Donors"]  # This keeps your /docs page beautifully organized
)


# We can move our Pydantic models here for now to keep things contained
class DonorIn(BaseModel):
    name: str
    age: int
    phone: str
    bg: str


class DonorOut(BaseModel):
    id: int
    name: str
    age: int
    bg: str
    lst_don: str


# Look how clean the route is! Just '/' because the prefix handles the '/donors' part
@router.post('/', response_model=DonorOut, status_code=status.HTTP_201_CREATED)
def add_donor(donor_data: DonorIn, db=Depends(get_db)):
    cursor = db.cursor()
    new_id = cursor.var(int)
    new_date = cursor.var(str)

    data = [donor_data.name, donor_data.age, donor_data.phone, donor_data.bg, new_id, new_date]
    cursor.callproc('p_add_donor', data)
    db.commit()  # Don't forget the commit!

    donor_data_dict = {
        'id': new_id.getvalue(),
        'name': donor_data.name,
        'age': donor_data.age,
        'bg': donor_data.bg,
        'lst_don': new_date.getvalue()
    }

    return donor_data_dict

# You would paste the rest of your GET, PUT, and DELETE routes here below...
# Just remember to change @app to @router and remove '/donors' from the URL path!