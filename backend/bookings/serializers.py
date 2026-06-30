from rest_framework import serializers
from .models import Booking
from sessions_app.serializers import SessionSerializer
from users.serializers import UserSerializer

class BookingSerializer(serializers.ModelSerializer):
    session_detail = SessionSerializer(source='session', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'session', 'status', 'booked_at', 'session_detail', 'user_detail')
        read_only_fields = ('id', 'user', 'status', 'booked_at')

    def create(self, validated_data):
        session = validated_data['session']
        if session.booking.filter(status='confirmed').count() >= session.max_participants:
            raise serializers.ValidationError({"session": "Session is fully booked."})
        return super().create(validated_data)
