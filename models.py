from pydantic import BaseModel


def pagination(skip: int = 0, limit: int = 3):

    result = {'skip': skip, 'limit': limit}
    return result


class FrameIn(BaseModel):

    name: str
    dimension: str
    retail_price: float
    wholesale_cost: float


class FrameOut(BaseModel):

    id: int
    name: str
    dimension: str
    retail_price: float


class CustomerIn(BaseModel):

    name: str
    phone: str
    ship_address: str


class CustomerOut(BaseModel):

    id: int
    name: str
    phone: str
    ship_address: str


class  UserIn(BaseModel):

    user_name: str
    password: str


class UserOut(BaseModel):

    user_name: str