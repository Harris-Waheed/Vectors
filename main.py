from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import inventory, customers, users
import uvicorn

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000','http://localhost:8000'],
                   allow_methods='*',
                   allow_headers='*',
                   allow_credentials=True
                   )

app.include_router(inventory.router)
app.include_router(customers.router)
app.include_router(users.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000)
