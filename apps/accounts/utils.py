import pyotp

def generate_otp():
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key)
    return totp.now()