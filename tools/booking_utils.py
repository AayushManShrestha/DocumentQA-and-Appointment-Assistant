from tools.validator import validate_field
from tools.date_utils import parse_natural_date
import json
import os

def save_booking(entry, filepath="data/appointments.json"):
    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    data.append(entry)

    with open(filepath, "w") as f:
        json.dump(data, f, indent = 2)

def step_name(user_input, data):
    data["name"] = user_input.strip()
    if not data["name"]:
        return "Invalid name. Please enter a valid name with a first and a last name. Example: Dummy dummy"
    return None

def step_email(user_input, data):
    data["email"] = user_input.strip()
    valid, err = validate_field(email=data["email"])
    if not valid:
        data.pop("email", None)
        return "Invalid email. Please enter a valid email address. Example: dummy@gmail.com"
    return None

def step_phone(user_input, data):
    data["phone"] = user_input.strip()
    valid, err = validate_field(phone=data["phone"])
    if not valid:
        data.pop("phone", None)
        return "Invalid phone number. Please enter a valid phone number for country Nepal. Example: +977-1234567890 or 1234567890"
    return None

def step_date(user_input, data):
    date_val = parse_natural_date(user_input.strip())
    if not date_val:
        return "Invalid date. Please enter a date like '2024-06-10' or 'next Monday'."
    data["date"] = date_val
    return None

def step_purpose(user_input, data):
    data["purpose"] = user_input.strip()
    valid, err = validate_field(purpose=data["purpose"])
    if not valid:
        data.pop("purpose", None)
        return "Please describe the purpose of your appointment in a few words."
    return None

step_handlers = {
    1: step_name,
    2: step_email,
    3: step_phone,
    4: step_date,
    5: step_purpose
}

def next_prompt_for_step(step):
    prompts = {
        1: "May I have your full name? Include first and last name",
        2: "Please enter your email address (e.g., john.doe@example.com).",
        3: "What's your phone number? Only Nepali numbers are accepted. You can include the country code (e.g., +9779812345678 or 9812345678).",
        4: "When would you like to book the appointment? You can type a specific date (e.g., 2024-06-10) or a phrase like 'next Monday'.",
        5: "Briefly describe the purpose of your appointment (e.g., dental checkup, consultation, etc.)."
    }
    return prompts.get(step, "")
