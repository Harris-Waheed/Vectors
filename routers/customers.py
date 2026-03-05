from fastapi import APIRouter, Depends, status, HTTPException
from models import CustomerIn, CustomerOut, pagination
from Database import get_db
import oracledb

router = APIRouter(prefix='/customers', tags=['Customers'])


@router.post('/', response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def add_customer(new_customer: CustomerIn, db=Depends(get_db)):

    cursor = db.cursor()
    new_id = cursor.var(int)

    cursor.callproc('p_add_customer', [new_customer.name, new_customer.phone, new_customer.ship_address, new_id])

    result = {

        'id': new_id.getvalue(),
        'name': new_customer.name,
        'phone': new_customer.phone,
        'ship_address': new_customer.ship_address
    }

    return result


@router.get('/', response_model=list[CustomerOut])
def display_customers(pagi: dict = Depends(pagination), db=Depends(get_db)):

    skip = pagi['skip']
    limit = pagi['limit']

    cursor = db.cursor()
    ref_cur = cursor.var(oracledb.CURSOR)
    cursor.callproc('p_display_customer', [ref_cur])
    result = ref_cur.getvalue()
    rows = result.fetchall()

    customers = []

    for row in rows:
        customer = {

            'id': row[0],
            'name': row[1],
            'phone': row[2],
            'ship_address': row[3]
        }
        customers.append(customer)

    return customers[skip: skip + limit]


@router.get('/{customer_id}', response_model=CustomerOut)
def display_customer(customer_id: int, db=Depends(get_db)):

    cursor = db.cursor()
    ref_cur = cursor.var(oracledb.CURSOR)
    cursor.callproc('p_display_customer', [ref_cur])
    result = ref_cur.getvalue()
    rows = result.fetchall()

    for row in rows:

        if row[0] == customer_id:
            customer = {

                'id': row[0],
                'name': row[1],
                'phone': row[2],
                'ship_address': row[3]
            }

            return customer
    raise HTTPException(status_code=404, detail='Id not found!')


@router.put('/{customer_id}')
def update_customer(customer_id: int, new_address: str, db=Depends(get_db)):

    cursor = db.cursor()
    count = cursor.var(int)
    cursor.callproc('p_update_customer', [customer_id, new_address, count])
    actual_count = count.getvalue()
    db.commit()

    if actual_count == 0:
        raise HTTPException(status_code=404, detail='Id Not Found!')

    result = {

        'id': customer_id,
        'new_address': new_address
    }

    return result


@router.delete('/{customer_id}')
def delete_customer(customer_id: int, db=Depends(get_db)):

    cursor = db.cursor()
    count = cursor.var(int)
    cursor.callproc('p_delete_customer', [customer_id, count])
    db.commit()
    actual_count = count.getvalue()

    if actual_count == 0:
        raise HTTPException(status_code=404, detail='Id Not Found!')

    result = {

        'id': customer_id,
        'status': 'Deleted!'
    }

    return result
