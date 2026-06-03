from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.notification_routes import router as notification_router
from app.routes.auth_routes import router as auth_router
from app.routes.patient_routes import router as patient_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.prescription_routes import router as prescription_router

from app.services.scheduler_service import start_scheduler

from app.services.whatsapp_service import send_whatsapp_message

app = FastAPI(title="SHMS Backend Sprint 2")


@app.on_event("startup")
async def startup_event():
    start_scheduler()
    print("Reminder Scheduler Started Successfully")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Routes
app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Auth"]
)

# Patient Routes
app.include_router(
    patient_router,
    prefix="/api/v1/patients",
    tags=["Patients"]
)

# Dashboard Routes
app.include_router(
    dashboard_router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

# Prescription Routes
app.include_router(
    prescription_router,
    prefix="/api/v1",
    tags=["Prescriptions"]
)

# Notification Routes
app.include_router(
    notification_router,
    prefix="/api/v1/notifications",
    tags=["Notifications"]
)


 

@app.get("/test-whatsapp")
def test_whatsapp():

    send_whatsapp_message(
        mobile="919705623697",
        medicine_name="Dolo 650",
        timing="Morning"
    )

    return {
        "message": "WhatsApp Sent"
    }
@app.get("/")
def home():
    return {
        "message": "SHMS Backend Running Successfully"
    }