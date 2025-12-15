from fastapi import FastAPI
import uvicorn
from app.routers import product_crud

app = FastAPI()
app.include_router(product_crud.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
