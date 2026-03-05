from fastapi import FastAPI
from routers import inventory, customers
import uvicorn

app = FastAPI()

app.include_router(inventory.router)
app.include_router(customers.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000)
