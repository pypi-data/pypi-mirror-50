from django.apps import AppConfig as BaseConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseConfig):
    name = "artek.templates"
    label = "artek_templates"
    verbose_name = _('Artek Templates')