import requests
import json
from django.conf import settings

class ZarinPalSandbox:

    def __init__(self):

        self.merchant_id = settings.MERCHANT_ID
        self.callback_url = 'http://127.0.0.1:8000/payment/verify/'  # آدرس بازگشتی پس از پرداخت
        self.payment_request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
        self.payment_verify_url = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
        self.payment_page_url = 'https://sandbox.zarinpal.com/pg/StartPay/{authority_code}/'
    # --------------------------------------
    def payment_request(self, amount, description='برداخت کاربر'):

        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "description": description,
            "callback_url": self.callback_url
        }

        headers = {
            'content-type': 'application/json'
        }

        try:
            response = requests.post(self.payment_request_url, headers=headers, data=json.dumps(payload), verify=False, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Payment request error: {e}")
            return {"errors": str(e)}
    # --------------------------------------
    def payment_verify(self, authority_code, amount):

        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority_code
        }

        headers = {
            'content-type': 'application/json'
        }

        try:
            response = requests.post(self.payment_verify_url, headers=headers, data=json.dumps(payload), verify=False, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Payment verify error: {e}")
            return {"errors": str(e)}
    # --------------------------------------
    def get_payment_page_url(self, authority_code):
        return self.payment_page_url.format(authority_code=authority_code)
# ----------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # callback_url = "https://maktabkhooneh.org/"
    zarinpal = ZarinPalSandbox()

    # Example usage:
    amount = 10000  # Amount in IRR
    description = "Test Payment"
    payment_request_response = zarinpal.payment_request(amount, description)
    print(payment_request_response)

    authority_code = payment_request_response['data'].get('authority')
    if authority_code:
        payment_page_url = zarinpal.get_payment_page_url(authority_code)
        print(f"Redirect user to: {payment_page_url}")

        # After user completes payment, verify it
        input("check validateion and press Enter to continue...")
        verification_response = zarinpal.payment_verify(authority_code, amount)
        print(verification_response)
    print("Done")
# ----------------------------------------------------------------------------------------------------------------
