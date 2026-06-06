from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(
    autoretry_for=(OSError, ConnectionError),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
)
def send_verification_email(email: str, code: str) -> int:
    """
    Emails the OTP code asynchronously (Celery) to the user.

    @shared_task decoration parameters:
    autoretry_for: In case of network error (OSError, ConnectionError) such as DNS or
    connection loss, the task will be automatically retried.
    retry_backoff: The interval between each retry increases exponentially (1s, 2s, 4s, ...).
    retry_kwargs: Up to 3 retries before final failure.

    send_mail parameters:
    fail_silently=False: In case of an error (e.g. SMTP), throw an exception to be seen in the
    celery_worker log; if True, the error will be silent.
    """
    return send_mail(
        subject="کد تأیید ثبت‌نام",
        message=(
            f"کد تأیید شما: {code}\n"
            "این کد تا ۱۰ دقیقه معتبر است."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
