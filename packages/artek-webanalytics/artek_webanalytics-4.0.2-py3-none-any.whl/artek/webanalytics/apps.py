from django.apps import AppConfig as BaseConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseConfig):
    name = "artek.webanalytics"
    label = "artek-webanalytics"
    verbose_name = _('Artek Web Analytics')