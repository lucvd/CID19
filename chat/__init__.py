__version__ = '0.9.7'

try:
    from django import VERSION as DJANGO_VERSION
    if DJANGO_VERSION >= (1, 7):
        default_app_config = 'chat.apps.ChatConfig'
    else:
        from directmessages.apps import populateInbox
        populateInbox()
except ImportError:
    pass
