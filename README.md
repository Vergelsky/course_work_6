# course_work_6

config проекта лежит в папке mailinger

Нужно прописать свои настройки почты, для отправки письма подтверждения регистрации:

или использовать эти

в settings.py

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

EMAIL_HOST = 'smtp.mail.ru'

EMAIL_PORT = 465

EMAIL_HOST_USER = 'skyprothebest@mail.ru'

EMAIL_HOST_PASSWORD = 'L38Shb5XVGehbWNH1rZX'

EMAIL_USE_SSL = True

EMAIL_SSL_CERTFILE = None

EMAIL_SSL_KEYFILE = None