from app.database.supabase_client import supabase


def create_patient(data, email):
    patient_data = data.model_dump(mode="json")
    patient_data["doctor_email"] = email

    result = (
        supabase
        .table("patients")
        .insert(patient_data)
        .execute()
    )

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
    update_data = data.model_dump(
        mode="json",
        exclude_unset=True
    )

    result = (
        supabase
        .table("patients")
        .update(update_data)
        .eq("mobile_number", mobile)
        .eq("doctor_email", email)
        .execute()
    )

    return result.data


def delete_patient(mobile, email):

    # Delete all prescriptions of this patient
    supabase.table("prescriptions") \
        .delete() \
        .eq("patient_mobile", mobile) \
        .eq("doctor_email", email) \
        .execute()

    # Delete patient
    result = (
        supabase.table("patients")
        .delete()
        .eq("mobile_number", mobile)
        .eq("doctor_email", email)
        .execute()
    )

    return result.data