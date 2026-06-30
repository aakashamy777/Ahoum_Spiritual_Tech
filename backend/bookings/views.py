from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer

from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booked_at')

    @method_decorator(ratelimit(key='user', rate='10/m', block=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'])
    def my(self, request):
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'cancelled':
            return Response({"detail": "Booking is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({"detail": "Booking cancelled successfully"})

    @action(detail=False, methods=['get'], url_path='creator-overview')
    def creator_overview(self, request):
        if request.user.role != 'creator':
            return Response({"detail": "Only creators can access this."}, status=status.HTTP_403_FORBIDDEN)
            
        # Bookings for sessions created by this user
        bookings = Booking.objects.filter(session__creator=request.user).order_by('-booked_at')
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
