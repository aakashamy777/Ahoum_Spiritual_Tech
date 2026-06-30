import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from bookings.models import Booking
from sessions_app.models import Session

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        session_id = request.data.get('session_id')
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
            
        if session.price <= 0:
            return Response({'error': 'Session is free, no payment needed'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create a pending booking first
        booking, created = Booking.objects.get_or_create(
            user=request.user,
            session=session,
            defaults={'status': 'pending'}
        )
        
        # Razorpay takes amount in paise (multiply by 100)
        amount = int(session.price * 100)
        
        data = {
            "amount": amount,
            "currency": "INR",
            "receipt": f"booking_{booking.id}",
        }
        
        try:
            order = client.order.create(data=data)
            return Response({
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'key': settings.RAZORPAY_KEY_ID,
                'booking_id': booking.id
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')
        booking_id = request.data.get('booking_id')
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.status = 'confirmed'
            booking.save()
            return Response({'status': 'Payment verified and booking confirmed'})
        except Exception as e:
            return Response({'error': 'Signature verification failed'}, status=status.HTTP_400_BAD_REQUEST)
