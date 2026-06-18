from datetime import date

from app.database.supabase_client import supabase


def get_dashboard_data(email):

    patients = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .execute()
    )

    total_patients = len(
        patients.data
    )

    today = date.today().isoformat()

    today_appointments = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .eq(
            "next_consultation_date",
            today
        )
        .execute()
    )

    confirmed = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .eq(
            "next_consultation_date",
            today
        )
        .eq(
            "appointment_status",
            "CONFIRMED"
        )
        .execute()
    )

    pending = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .eq(
            "next_consultation_date",
            today
        )
        .eq(
            "appointment_status",
            "PENDING"
        )
        .execute()
    )

    cancelled = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .eq(
            "appointment_status",
            "CANCELLED"
        )
        .execute()
    )

    prescriptions = (
        supabase
        .table("prescriptions")
        .select("*")
        .eq("doctor_email", email)
        .execute()
    )

    return {

        "total_patients":
        total_patients,

       # "today_appointments":
       # len(today_appointments.data),

       "today_appointments":
       len(confirmed.data),

        "confirmed_appointments":
        len(confirmed.data),

        "pending_appointments":
        len(pending.data),

        "cancelled_appointments":
        len(cancelled.data),

        "active_prescriptions":
        len(prescriptions.data),

        "pending_reminders":
        len(pending.data)
    }