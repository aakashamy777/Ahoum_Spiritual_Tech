from rest_framework import serializers
from .models import Session
from users.serializers import UserSerializer

class SessionSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    booking_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Session
        fields = '__all__'
        read_only_fields = ('id', 'creator', 'created_at', 'updated_at', 'booking_count')
