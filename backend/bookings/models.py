from django.db import models
from users.models import User
from sessions_app.models import Session

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='booking') # changed from bookings to avoid clash or just rely on default
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'session')
        
    def __str__(self):
        return f"{self.user.username} - {self.session.title}"
