import secrets
import string

def generate_reset_token(length=32):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

