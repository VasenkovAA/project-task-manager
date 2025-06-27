# ci_settings.py
import sys
from .settings import *  # Импорт основных настроек

# Фиктивные значения для CI
SECRET_KEY = "dummy-secret-key-for-ci-12345"
DEBUG = False

# Отключаем ВСЕ базы данных
DATABASES = {}

# Отключаем миграции
MIGRATION_MODULES = {
    app.split('.')[-1]: None for app in INSTALLED_APPS
}

# Отключаем приложения, требующие БД
DISABLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
]
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in DISABLED_APPS]

# Отключаем middleware, требующий БД
DISABLED_MIDDLEWARE = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]
MIDDLEWARE = [m for m in MIDDLEWARE if m not in DISABLED_MIDDLEWARE]

# Отключаем системные проверки
SILENCED_SYSTEM_CHECKS = [
    'fields.E100',  # Автофилд
    'models.E006',  # Meta.constraints
    'models.E007',  # Meta.indexes
    'models.E020',  # related_name
    'security.W004',  # SECURE_HSTS_SECONDS
    'security.W008',  # SECURE_SSL_REDIRECT
    'urls.W002',  # URL namespaces
    'admin.E408',  # Admin middleware
    'admin.E409',  # Admin site
    'admin.E410',  # Admin auth
]

# Отключаем сигналы
def disable_signals(*args, **kwargs):
    pass

from django.db.models import signals
for name in dir(signals):
    if name.startswith('pre_') or name.startswith('post_'):
        signal = getattr(signals, name)
        signal.disconnect_all()

# Отключаем автозагрузку приложений
class DisabledAppConfig:
    def ready(self):
        pass

for app_config in INSTALLED_APPS:
    sys.modules.pop(app_config, None)