from fastapi import FastAPI
from first_api.api.basketball.routes import router as basketball_router
from first_api.api.survey.routes import router as survey_router

app = FastAPI(title="First API", version="0.1.0")

app.include_router(basketball_router, prefix="/basketball", tags=["basketball-tracker"])
app.include_router(survey_router, prefix="/survey", tags=["survey"])
