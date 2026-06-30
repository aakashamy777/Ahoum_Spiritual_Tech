from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Session
from .serializers import SessionSerializer
from .permissions import IsCreator, IsOwnerOrReadOnly

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.filter(is_active=True).annotate(booking_count=Count('booking')).order_by('scheduled_at')
    serializer_class = SessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, IsCreator]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsCreator, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
        
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
