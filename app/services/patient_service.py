from app.database.supabase_client import supabase


def create_patient(data, email):
    patient_data = data.dict()
    patient_data["doctor_email"] = email

    result = supabase.table("patients").insert(patient_data).execute()
    return result.data


def get_all_patients(email):
    result = (
        supabase.table("patients")
        .select("*")
        .eq("doctor_email", email)
        .execute()
    )
    return result.data


def get_patient_by_mobile(mobile, email):
    result = (
        supabase.table("patients")
        .select("*")
        .eq("mobile_number", mobile)
        .eq("doctor_email", email)
        .execute()
    )
    return result.data


def update_patient(mobile, data, email):
    result = (
        supabase.table("patients")
        .update(data.dict())
        .eq("mobile_number", mobile)
        .eq("doctor_email", email)
        .execute()
    )
    return result.data


def delete_patient(mobile, email):
    result = (
        supabase.table("patients")
        .delete()
        .eq("mobile_number", mobile)
        .eq("doctor_email", email)
        .execute()
    )
    return result.data