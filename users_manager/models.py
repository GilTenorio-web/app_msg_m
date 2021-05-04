from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user_age=models.IntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    ACADEMIC=1
    RS_USER=2
    VL_GROUP=3
    ROL = (
       (ACADEMIC, 'Academico'),
       (RS_USER, 'Usuario RS'),
       (VL_GROUP, 'Grupo vulnerable'),
    )
    user_rol=models.PositiveSmallIntegerField(choices=ROL,default=ACADEMIC,)

    MALE=1
    FEMALE=2
    OTHER=3
    GENDER = (
        (MALE, 'Hombre'),
        (FEMALE, 'Mujer'),
        (OTHER, 'Otro'),
    )
    user_gender=models.PositiveSmallIntegerField(choices=GENDER,default=FEMALE,)

    class Meta:
        verbose_name='profile'
        verbose_name_plural='profiles'