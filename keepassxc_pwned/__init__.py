from .password import lookup_pwned


def check_password(password: str) -> int:
    return lookup_pwned(password)
