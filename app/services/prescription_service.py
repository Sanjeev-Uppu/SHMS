from app.database.supabase_client import supabase


# CREATE PRESCRIPTION
def create_prescription(data, email):

    prescription_data = {
        "patient_mobile": data.patient_mobile,
        "doctor_name": data.doctor_name,
        "notes": data.notes,
        "doctor_email": email
    }

    prescription = (
        supabase
        .table("prescriptions")
        .insert(prescription_data)
        .execute()
    )

    prescription_id = prescription.data[0]["id"]

    medicines = []

    for med in data.medicines:
        item = med.dict()
        item["prescription_id"] = prescription_id
        medicines.append(item)

    supabase.table(
        "prescription_items"
    ).insert(
        medicines
    ).execute()

    return {
        "message": "Prescription created successfully",
        "prescription_id": prescription_id
    }


# GET ALL PRESCRIPTIONS
def get_all_prescriptions(email):

    result = (
        supabase
        .table("prescriptions")
        .select("*")
        .eq("doctor_email", email)
        .execute()
    )

    return result.data


# GET PRESCRIPTION BY ID
def get_prescription(id, email):

    prescription = (
        supabase
        .table("prescriptions")
        .select("*")
        .eq("id", id)
        .eq("doctor_email", email)
        .single()
        .execute()
    )

    medicines = (
        supabase
        .table("prescription_items")
        .select("*")
        .eq("prescription_id", id)
        .execute()
    )

    return {
        "prescription": prescription.data,
        "medicines": medicines.data
    }


# UPDATE MEDICINE
def update_medicine(item_id, data):

    result = (
        supabase
        .table("prescription_items")
        .update(data.dict())
        .eq("id", item_id)
        .execute()
    )

    return result.data


# UPDATE PRESCRIPTION
def update_prescription(id, data, email):

    prescription_data = {
        "doctor_name": data.doctor_name,
        "notes": data.notes
    }

    supabase.table(
        "prescriptions"
    ).update(
        prescription_data
    ).eq(
        "id", id
    ).eq(
        "doctor_email", email
    ).execute()

    supabase.table(
        "prescription_items"
    ).delete().eq(
        "prescription_id", id
    ).execute()

    medicines = []

    for med in data.medicines:
        item = med.dict()
        item["prescription_id"] = id
        medicines.append(item)

    supabase.table(
        "prescription_items"
    ).insert(
        medicines
    ).execute()

    return {
        "message": "Prescription updated successfully"
    }


# DELETE MEDICINE
def delete_medicine(item_id):

    result = (
        supabase
        .table("prescription_items")
        .delete()
        .eq("id", item_id)
        .execute()
    )

    return result.data


# DELETE PRESCRIPTION
def delete_prescription(id, email):

    result = (
        supabase
        .table("prescriptions")
        .delete()
        .eq("id", id)
        .eq("doctor_email", email)
        .execute()
    )

    return result.data