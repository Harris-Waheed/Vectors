from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import inventory, customers
import uvicorn

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origin='http://localhost:3000',
                   allow_methods='*',
                   allow_header='*',
                   allow_credentials=True
                   )

app.include_router(inventory.router)
app.include_router(customers.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000)
