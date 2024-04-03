from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Validators
def validate_id_num(value):
    try:
        if len(value) != 10:
            raise
        for i in tuple(value):
            int(i)
    except:
        raise ValidationError(
            _("%(value)s is not a number"),
            params={"value": value},
        )


# Create your models here.
class Doctor(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=10, validators=[validate_id_num])
    profile_picture = models.ImageField(upload_to='images/')


# class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    image = models.ImageField(default='default.jpg',  
#                                      upload_to='profile_pics')
#    def __str__(self):
#       return f'{self.user.username} Profile'