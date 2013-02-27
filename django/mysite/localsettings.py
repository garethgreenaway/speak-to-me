import os

CURRENT_DIR = "/home/ggreenaway/code/speak-to-me/django"

UPLOAD_DIR = os.path.join(CURRENT_DIR, 'upload')
STORAGE_ROOT = os.path.join(CURRENT_DIR, 'storage')
STORAGE_URL = '/media/'

TEMPLATE_DIRS = (
    '/home/ggreenaway/code/speak-to-me/html',
)

STATICFILES_DIRS = (
    '/home/ggreenaway/code/speak-to-me/html',
)
