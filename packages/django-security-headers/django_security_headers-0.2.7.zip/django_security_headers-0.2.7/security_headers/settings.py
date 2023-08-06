# -*- coding: utf-8 -*-
import django
import os
from packaging import version


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "security-headers"

DEBUG = True

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "security_headers.urls"

INSTALLED_APPS = [
    "security_headers",
    "sslserver",  # For development and local testing only
    "csp",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

if version.parse(django.get_version()) < version.parse("2.1"):
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "csp.middleware.CSPMiddleware",
        "security_headers.middleware.extra_security_headers_middleware",
        "django_cookies_samesite.middleware.CookiesSameSite",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]
else:
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "csp.middleware.CSPMiddleware",
        "security_headers.middleware.extra_security_headers_middleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

STATIC_URL = "/static/"

# SecurityMiddleware settings
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = "__Host-csrftoken"
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 183 * 24 * 60 * 60  # 6-month default
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

# Django 1.11 patches for Django 2.1 functionality
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# Sample Django-CSP settings
CSP_DEFAULT_SRC = ["'self'"]
CSP_FONT_SRC = ["'self'"]
CSP_FRAME_SRC = ["*"]
CSP_IMG_SRC = ["*", "data:"]
CSP_MEDIA_SRC = ["*", "data:"]
CSP_SCRIPT_SRC = ["'self'"]
CSP_STYLE_SRC = ["'self'"]
CSP_INCLUDE_NONCE_IN = ["script-src", "style-src"]
CSP_UPGRADE_INSECURE_REQUESTS = True
CSP_BLOCK_ALL_MIXED_CONTENT = True
CSP_REPORT_PERCENTAGE = 0.1

# Default extra security header settings
REFERRER_POLICY = "same-origin"
FEATURE_POLICY = [
    "autoplay 'none'",
    "camera 'none'",
    "display-capture 'none'",
    "document-domain 'none'",
    "encrypted-media 'none'",
    "fullscreen *",
    "geolocation 'none'",
    "microphone 'none'",
    "midi 'none'",
    "payment 'none'",
    "vr *",
]
