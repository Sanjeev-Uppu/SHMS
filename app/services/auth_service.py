from app.database.supabase_client import supabase
from app.auth.password_handler import hash_password, verify_password
from app.auth.jwt_handler import create_access_token


def signup_user(data):

    # Check if passwords match
    if data.password != data.confirm_password:
        return {
            "success": False,
            "message": "Passwords do not match"
        }

    # Check existing email
    existing = supabase.table("doctors") \
        .select("*") \
        .eq("email", data.email) \
        .execute()

    if existing.data:
        return {
            "success": False,
            "message": "Email already exists"
        }

    # Hash password
    hashed = hash_password(data.password)

    # User data
    user_data = {
        "full_name": data.full_name,
        "hospital_name": data.hospital_name,
        "email": data.email,
        "phone_number": data.phone_number,
        "hashed_password": hashed
    }

    # Insert into database
    supabase.table("doctors").insert(user_data).execute()

    # Generate JWT token
    token = create_access_token({
        "sub": data.email
    })

    return {
        "success": True,
        "message": "Doctor registered successfully",
        "token": token
    }


def login_user(data):

    # Check email
    result = supabase.table("doctors") \
        .select("*") \
        .eq("email", data.email) \
        .execute()

    if not result.data:
        return {
            "success": False,
            "message": "Invalid email"
        }

    user = result.data[0]

    # Verify password
    if not verify_password(
        data.password,
        user["hashed_password"]
    ):
        return {
            "success": False,
            "message": "Invalid password"
        }

    # Generate JWT token
    token = create_access_token({
        "sub": user["email"]
    })

    return {
        "success": True,
        "message": "Login successful",
        "token": token
    }