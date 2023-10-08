from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from datetime import date, timedelta

from modules.services.utils import unique_slugify

User = get_user_model()


class Profile(models.Model):
    pass
