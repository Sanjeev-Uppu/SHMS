from datetime import date, timedelta
from app.database.supabase_client import supabase


def get_due_reminders():

    reminders = []

    # ==========================================
    # MEDICINE REMINDERS
    # ==========================================

    prescriptions = (
        supabase
        .table("prescriptions")
        .select("*")
        .execute()
    )

    if prescriptions.data:

        for prescription in prescriptions.data:

            mobile = prescription.get("patient_mobile")

            # TESTING ONLY
            if mobile != "9059686278":
                continue

            patient_name = "Patient"

            try:

                patient = (
                    supabase
                    .table("patients")
                    .select("*")
                    .eq("mobile_number", mobile)
                    .execute()
                )

                if patient.data:

                    patient_name = (
                        patient.data[0].get("patient_name")
                        or "Patient"
                    )

            except Exception as e:

                print(
                    f"Patient Fetch Error: {e}"
                )

            medicines = (
                supabase
                .table("prescription_items")
                .select("*")
                .eq(
                    "prescription_id",
                    prescription["id"]
                )
                .execute()
            )

            for medicine in medicines.data:

                reminders.append({
                    "type": "medicine",
                    "patient_name": patient_name,
                    "mobile": mobile,
                    "medicine_name": medicine.get(
                        "medicine_name"
                    ),
                    "timing": "Testing"
                })

    # ==========================================
    # CONSULTATION REMINDERS
    # ==========================================

    tomorrow = (
        date.today() + timedelta(days=1)
    ).isoformat()

    consultation_patients = (
        supabase
        .table("patients")
        .select("*")
        .eq(
            "next_consultation_date",
            tomorrow
        )
        .execute()
    )

    if consultation_patients.data:

        for patient in consultation_patients.data:

            mobile = patient.get(
                "mobile_number"
            )

            # TESTING ONLY
            if mobile != "9059686278":
                continue

            reminders.append({
                "type": "consultation",
                "patient_name": patient.get(
                    "patient_name"
                ),
                "mobile": mobile,
                "next_consultation_date": patient.get(
                    "next_consultation_date"
                )
            })

    print(
        f"Total Reminders Found: {len(reminders)}"
    )

    return reminders