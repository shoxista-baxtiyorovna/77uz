from .base import *  # noqa

ALLOWED_HOSTS = ["*"]
DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True

# SWAGGER_SETTINGS = {
#     "SECURITY_DEFINITIONS": {
#         "[Bearer {JWT}]": {
#             "name": "Authorization",
#             "type": "apiKey",
#             "in": "header",
#         }
#     },
#     "USE_SESSION_AUTH": False,
#     "APIS_SORTER": "alpha",
#     "SUPPORTED_SUBMIT_METHODS": ["get", "post", "put", "delete", "patch"],
#     "OPERATIONS_SORTER": "alpha",
# }


SPECTACULAR_SETTINGS = {
    "TITLE": "77uz API",
    "DESCRIPTION": "Bu yerda loyihamdagi API endpointlar jamlangan",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        {"name": "Accounts", "description": "Foydalanuvchi autentifikatsiyasi va profillar"},
        {"name": "Store", "description": "Mahsulotlar, buyurtmalar va to‘lovlar"},
        {"name": "Common", "description": "Umumiy endpointlar (masalan, settings, static)"},
    ],
}


INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
