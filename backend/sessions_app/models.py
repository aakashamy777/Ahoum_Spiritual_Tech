from django.db import models
from users.models import User

class Session(models.Model):
    CATEGORY_CHOICES = (
        ('meditation', 'Meditation'),
        ('yoga', 'Yoga'),
        ('therapy', 'Therapy'),
        ('coaching', 'Coaching'),
        ('other', 'Other'),
    )
    
    creator = models.ForeignKey(User, related_name='created_sessions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_minutes = models.IntegerField()
    scheduled_at = models.DateTimeField()
    max_participants = models.IntegerField()
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
