from keepassxc_pwned.password import lookup_pwned


def check_password(password: str) -> int:
    _, count = lookup_pwned(password)
    return count
