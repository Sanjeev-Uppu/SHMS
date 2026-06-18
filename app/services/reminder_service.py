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

            mobile = prescription.get(
                "patient_mobile"
            )

            patient_name = "Patient"

            try:

                patient = (
                    supabase
                    .table("patients")
                    .select("*")
                    .eq(
                        "mobile_number",
                        mobile
                    )
                    .execute()
                )

                if patient.data:

                    patient_name = (
                        patient.data[0].get(
                            "patient_name"
                        )
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

                timings = []

                if medicine.get("early_morning"):
                    timings.append(
                        "Early Morning (6:00 AM - 7:00 AM)"
                    )

                if medicine.get("morning"):
                    timings.append(
                        "Morning (8:00 AM - 9:00 AM)"
                    )

                if medicine.get("afternoon"):
                    timings.append(
                        "Afternoon (1:00 PM - 2:00 PM)"
                    )

                if medicine.get("night"):
                    timings.append(
                        "Night (8:00 PM - 9:00 PM)"
                    )

                food_instruction = ""

                if medicine.get("before_food"):
                    food_instruction = (
                        "Before Food"
                    )

                elif medicine.get("after_food"):
                    food_instruction = (
                        "After Food"
                    )

                reminders.append({

                    "type": "medicine",

                    "patient_name":
                    patient_name,

                    "mobile":
                    mobile,

                    "medicine_name":
                    medicine.get(
                        "medicine_name"
                    ),

                    "timings":
                    ", ".join(
                        timings
                    ),

                    "food_instruction":
                    food_instruction,

                    "duration_days":
                    medicine.get(
                        "duration_days"
                    ),

                    "remarks":
                    medicine.get(
                        "remarks"
                    )
                })

    # ==========================================
    # CONSULTATION REMINDERS
    # ==========================================

    tomorrow = (
        date.today()
        + timedelta(days=1)
    ).isoformat()

    consultation_patients = (
        supabase
        .table("patients")
        .select("*")
        .eq(
            "next_consultation_date",
            tomorrow
        )
        .eq(
            "appointment_status",
            "PENDING"
        )
        .execute()
    )

    if consultation_patients.data:

        for patient in consultation_patients.data:

            reminders.append({

                "type":
                "consultation",

                "patient_name":
                patient.get(
                    "patient_name"
                ),

                "mobile":
                patient.get(
                    "mobile_number"
                ),

                "next_consultation_date":
                patient.get(
                    "next_consultation_date"
                )
            })

    print(
        f"Total Reminders Found: "
        f"{len(reminders)}"
    )

    return reminders