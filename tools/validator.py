from pydantic import BaseModel, EmailStr, Field, ValidationError

class UserAppointmentInfo(BaseModel):
    # Contact Info Fields
    name: str = Field(..., min_length=3, max_length=100, pattern=r'^[A-Za-z]+ [A-Za-z]+$')
    email: EmailStr
    phone: str = Field(..., pattern=r'^(\+?977[-]?)?\d{10}$')
    # Appointment Details Fields
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    purpose: str = Field(..., min_length=5, max_length=500)

def validate_field(name="dummy dummy", email="dummy@example.com", phone="+977-1234567890", date="2030-01-01", purpose="dummy purpose"):
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "date": date,
        "purpose": purpose
    }
    try:
        UserAppointmentInfo(**data)
        return True, ""
    except ValidationError as e:
        error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return False, "; ".join(error_messages)