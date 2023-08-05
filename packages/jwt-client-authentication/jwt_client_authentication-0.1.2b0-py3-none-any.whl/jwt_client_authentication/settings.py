from django.conf import settings

default_jwt_settings= {
    'CAS_URL':  'http://192.168.99.100:8010'
}

settings = getattr(settings, 'JWT_SETTINGS', default_jwt_settings)



