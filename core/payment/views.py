from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import Payment, PeymentStatusType
from .zarinpal_client import ZarinPalSandbox
from order.models import Order, OrderStatusTypes
# --------------------------------------------------------------------------------------------------------
class PaymentVerifyView(View):
    
    def get(self, request):

        authority_code = request.GET.get('Authority')
        status = request.GET.get('Status')
        payment_obj = get_object_or_404(Payment, authority_code=authority_code)
        zarinpal = ZarinPalSandbox()
        verification_response = zarinpal.payment_verify(authority_code, int(payment_obj.amount))
        order = get_object_or_404(Order, payment=payment_obj)

        if status == 'OK':
            if verification_response['data'].get('code') in [100, 101] :
                payment_obj.status = PeymentStatusType.SUCCESS.value  # موفق
                payment_obj.ref_id = verification_response['data'].get('ref_id')
                payment_obj.response_json = verification_response
                payment_obj.response_code = verification_response['data'].get('code')
                payment_obj.save()
                order.status = OrderStatusTypes.SHIPPED.value
                order.save()
                return redirect('order:checkout-complete')
        
        elif status == 'NOK':
            payment_obj.status = PeymentStatusType.FAILED.value  # ناموفق
            payment_obj.response_json = verification_response
            # payment_obj.response_code = verification_response['data'].get('code')
            payment_obj.save()
            order.status = OrderStatusTypes.CANCELED.value
            order.save()
            return redirect('order:checkout-failed')

# --------------------------------------------------------------------------------------------------------
