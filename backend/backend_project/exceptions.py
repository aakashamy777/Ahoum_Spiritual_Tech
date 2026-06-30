from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class RateLimitExceeded(APIException):
    status_code = 429
    default_detail = _('Rate limit exceeded, try again later.')
    default_code = 'throttled'
