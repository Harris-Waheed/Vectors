from fastapi import APIRouter, Depends, status, HTTPException
from models import FrameIn, FrameOut, pagination
from Database import get_db
import oracledb

router = APIRouter(prefix='/inventory', tags=['Inventory'])


@router.post('/', response_model=FrameOut, status_code=status.HTTP_201_CREATED)
def add_frames(new_frame: FrameIn, db=Depends(get_db)):

    cursor = db.cursor()
    new_id = cursor.var(int)

    cursor.callproc('p_add_inventory', [new_frame.name, new_frame.dimension, new_frame.retail_price,
                                        new_frame.wholesale_cost, new_id])

    result = {

        'id': new_id.getvalue(),
        'name': new_frame.name,
        'dimension': new_frame.dimension,
        'retail_price': new_frame.retail_price
    }

    return result


@router.get('/', response_model=list[FrameOut])
def display_inventory(pagi: dict = Depends(pagination), db=Depends(get_db)):

    skip = pagi['skip']
    limit = pagi['limit']

    cursor = db.cursor()
    ref_cur = cursor.var(oracledb.CURSOR)
    cursor.callproc('p_display_inventory', [ref_cur])
    result = ref_cur.getvalue()
    rows = result.fetchall()

    inventory = []

    for row in rows:

        product = {

            'id': row[0],
            'name': row[1],
            'dimension': row[2],
            'retail_price': row[3]
        }
        inventory.append(product)

    return inventory[skip: skip+limit]


@router.get('/{item_id}', response_model=FrameOut)
def display_product(item_id: int, db=Depends(get_db)):

    cursor = db.cursor()
    ref_cur = cursor.var(oracledb.CURSOR)
    cursor.callproc('p_display_inventory', [ref_cur])
    result = ref_cur.getvalue()
    rows = result.fetchall()

    for row in rows:

        if row[0] == item_id:

            product = {

                'id': row[0],
                'name': row[1],
                'dimension': row[2],
                'retail_price': row[3]
            }

            return product
    raise HTTPException(status_code=404, detail='Id not found!')
