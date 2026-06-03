from datetime import datetime, timedelta

from app.database.supabase_client import supabase
from app.services.whatsapp_service import send_whatsapp_message


def process_reminders():

    try:

        print(
            f"\nChecking reminders at {datetime.now()}"
        )

        current_hour = datetime.now().hour
        today = datetime.now().date()

        prescriptions = (
            supabase
            .table("prescriptions")
            .select("*, prescription_items(*)")
            .execute()
        )

        if not prescriptions.data:
            print("No prescriptions found")
            return

        for prescription in prescriptions.data:

            mobile = prescription["patient_mobile"]

            created_at = datetime.fromisoformat(
                prescription["created_at"].replace("Z", "+00:00")
            )

            for medicine in prescription["prescription_items"]:

                medicine_name = medicine["medicine_name"]

                duration = (
                    medicine.get("duration_days") or 0
                )

                expiry_date = (
                    created_at.date()
                    + timedelta(days=duration)
                )

                if today > expiry_date:
                    continue

                # Early Morning - 6 AM
                if (
                    medicine.get("early_morning")
                    and current_hour == 6
                ):
                    send_reminder(
                        mobile,
                        medicine_name,
                        "Early Morning"
                    )

                # Morning - 9 AM
                if (
                    medicine.get("morning")
                    and current_hour == 9
                ):
                    send_reminder(
                        mobile,
                        medicine_name,
                        "Morning"
                    )

                # Afternoon - 1 PM
                if (
                    medicine.get("afternoon")
                    and current_hour == 13
                ):
                    send_reminder(
                        mobile,
                        medicine_name,
                        "Afternoon"
                    )

                # Night - 9 PM
                if (
                    medicine.get("night")
                    and current_hour == 21
                ):
                    send_reminder(
                        mobile,
                        medicine_name,
                        "Night"
                    )

    except Exception as e:
        print(
            f"Reminder Error: {str(e)}"
        )


def send_reminder(
    mobile,
    medicine_name,
    timing
):

    print(
        f"""
==================================
SENDING WHATSAPP REMINDER

Mobile   : {mobile}
Medicine : {medicine_name}
Timing   : {timing}

==================================
"""
    )

    send_whatsapp_message(
        mobile=mobile,
        medicine_name=medicine_name,
        timing=timing
    )