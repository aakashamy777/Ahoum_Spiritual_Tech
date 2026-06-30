from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sessions_app.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('users.urls')),
    path('api/payments/', include('payments.urls')),
    path('accounts/', include('allauth.urls')),
]
