from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.utils.translation import ugettext as _
from ohm2_handlers_light.models import BaseModel
from . import managers
from . import settings



"""
class Model(BaseModel):
	pass
"""
class Configuration(models.Model):
    key = models.CharField(max_length=50, default='')
    value = models.CharField(max_length=50, default='')




