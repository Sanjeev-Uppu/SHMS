from app.database.supabase_client import supabase

def create_patient(data):
    result = supabase.table("patients").insert(data.dict()).execute()
    return result.data

def get_all_patients():
    result = supabase.table("patients").select("*").execute()
    return result.data

def get_patient_by_mobile(mobile):
    result = supabase.table("patients").select("*").eq("mobile_number", mobile).execute()
    return result.data

def update_patient(mobile, data):
    result = supabase.table("patients").update(data.dict()).eq("mobile_number", mobile).execute()
    return result.data

def delete_patient(mobile):
    result = supabase.table("patients").delete().eq("mobile_number", mobile).execute()
    return result.data