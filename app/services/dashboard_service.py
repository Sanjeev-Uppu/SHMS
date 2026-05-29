from app.database.supabase_client import supabase

def get_dashboard_data():
    patients = supabase.table("patients").select("*").execute()

    return {
        "total_patients": len(patients.data),
        "today_appointments": 0,
        "active_prescriptions": 0,
        "pending_reminders": 0
    }