import os

DEBUG = False
ALLOWED_HOSTS = ['3.144.135.54']

# Security for reverse proxy/HTTPS
CSRF_TRUSTED_ORIGINS = ['http://3.144.135.54', 'https://3.144.135.54']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Enable after HTTPS is configured and TLS terminates at Nginx:
# SECURE_SSL_REDIRECT = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
        'HOST': os.environ.get('DBHOST', '127.0.0.1'),
        'PORT': os.environ.get('DBPORT', '5432'),
        'OPTIONS': {
            # Require SSL when connecting to managed Postgres (e.g., Amazon RDS)
            'sslmode': 'require',
            # Optionally pin CA certificate if you download it to the server:
            # 'sslrootcert': '/etc/ssl/certs/rds-combined-ca-bundle.pem',
        },

    }
}