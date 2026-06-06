import secrets
from django.core.cache import cache
from django.core.exceptions import ValidationError
# -------------------------------------
OTP_TTL = 600  # 10 minutes
VERIFIED_TTL = 1800  # 30 minutes
RATE_LIMIT_TTL = 900  # 15 minutes
RATE_LIMIT_MAX = 3
# -------------------------------------
def _normalize_email(email: str) -> str:

    """Synchronizes email to keep Redis keys consistent."""

    return email.strip().lower()
# -------------------------------------
def _otp_key(email: str) -> str:

    """Redis key to store temporary OTP code."""

    return f"otp:{_normalize_email(email)}"
# -------------------------------------
def _verified_key(email: str) -> str:

    """Redis key for marking email as verified."""

    return f"verified:{_normalize_email(email)}"
# -------------------------------------
def _rate_limit_key(email: str) -> str:

    """Redis key for counting the number of OTP requests."""

    return f"otp_rate:{_normalize_email(email)}"
# -------------------------------------
def generate_otp() -> str:

    """Generates a random 6-digit code."""

    return f"{secrets.randbelow(1_000_000):06d}"
# -------------------------------------
def store_otp(email: str, code: str) -> None:

    """Stores the OTP code in Redis with an expiration time of 10 minutes."""

    cache.set(_otp_key(email), code, timeout=OTP_TTL)
# -------------------------------------
def issue_otp(email: str) -> str:

    """Creates new code, checks rate limit, and stores in Redis."""

    check_rate_limit(email)
    code = generate_otp()
    store_otp(email, code)
    record_otp_request(email)
    return code
# -------------------------------------
def verify_otp(email: str, code: str) -> bool:

    """Compares the code with the Redis value; if true, deletes it."""

    key = _otp_key(email)
    stored = cache.get(key)
    if stored is None or stored != code:
        return False
    cache.delete(key)
    return True
# -------------------------------------
def mark_email_verified(email: str) -> None:

    """After OTP verification, marks the email as verified in Redis for up to 30 minutes."""

    cache.set(_verified_key(email), True, timeout=VERIFIED_TTL)
# -------------------------------------
def is_email_verified(email: str) -> bool:

    """Checks if the email is valid during the code verification phase."""

    return cache.get(_verified_key(email)) is True
# -------------------------------------
def clear_signup_state(email: str) -> None:

    """After successful registration, deletes all temporary keys for this email from Redis."""

    cache.delete(_otp_key(email))
    cache.delete(_verified_key(email))
    cache.delete(_rate_limit_key(email))
# -------------------------------------
def check_rate_limit(email: str) -> None:

    """If there are more than 3 OTP requests in 15 minutes, it throws ValidationError."""

    if cache.get(_rate_limit_key(email), 0) >= RATE_LIMIT_MAX:
        raise ValidationError(
            "تعداد درخواست‌ها بیش از حد مجاز است. لطفاً ۱۵ دقیقه دیگر تلاش کنید.",
            code="rate_limit",
        )
# -------------------------------------
def record_otp_request(email: str) -> None:

    """Increments the OTP request counter by one (for rate limit)."""    

    key = _rate_limit_key(email)
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=RATE_LIMIT_TTL)
