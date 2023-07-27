import re


def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[A-Z]", password):
        return False

    return True


def is_valid_name(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z\s]+$", name))


def is_valid_phone(phone: str) -> bool:
    return bool(re.match(r"^\d{10}$", phone))


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))
