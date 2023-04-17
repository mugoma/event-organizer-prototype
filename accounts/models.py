from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(
        validators=[EmailValidator(allowlist=['minerva.edu'], )])
