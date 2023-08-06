from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class EpicCoreConfig(AppConfig):
    name = 'epic_admin'
    verbose_name = _('Administration')