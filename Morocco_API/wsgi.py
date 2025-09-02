import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Morocco_API.settings')

application = get_wsgi_application()
if os.getenv('DJANGO_ENVIRONMENT') == 'production':
    from whitenoise import WhiteNoise
    from django.conf import settings
    application = WhiteNoise(application, root=settings.STATIC_ROOT)