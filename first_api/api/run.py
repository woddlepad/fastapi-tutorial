from fastapi import FastAPI
from first_api.api.basketball.routes import router as basketball_router

app = FastAPI(title="First API", version="0.1.0")

app.include_router(basketball_router, prefix="/basketball", tags=["basketball-tracker"])


@app.get("/")
def add_two_numbers(a: int, b: int):
    return {"sum": a + b}
