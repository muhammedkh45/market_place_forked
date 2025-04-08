from fastapi import FastAPI
from app.endpoints import users, transactions, search, logs

app = FastAPI(title="Distributed Marketplace API")

# Include routers from different endpoints
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Distributed Marketplace API"}
