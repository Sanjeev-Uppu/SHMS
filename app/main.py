from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.notification_routes import router as notification_router
from app.routes.auth_routes import router as auth_router
from app.routes.patient_routes import router as patient_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.prescription_routes import router as prescription_router

from app.routes.consultation_routes import router as consultation_router

from app.routes.search import router as search_router
 

 

from app.routes.reminder_routes import router as reminder_router

 
app = FastAPI(title="SHMS Backend Sprint 2")


 


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",
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

app.include_router(
    consultation_router,
    prefix="/api/v1"
)

app.include_router(
    reminder_router
)
 

app.include_router(
    auth_router,
    prefix="/api/v1/auth"
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

app.include_router(
    search_router,
    prefix="/api/v1",
    tags=["Search"]
)
@app.get("/")
def home():
    return {
        "message": "SHMS Backend Running Successfully"
    }