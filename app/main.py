from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import router as auth_router
from app.routes.patient_routes import router as patient_router
from app.routes.dashboard_routes import router as dashboard_router

app = FastAPI(title="SHMS Backend Sprint 1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(patient_router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/")
def home():
    return {"message": "SHMS Backend Running"}