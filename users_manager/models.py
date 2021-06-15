from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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

    def __str__(self):
        return '{}'.format(self.user)
    
class Archivo(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE)
    file = models.FileField(upload_to="archivos/", null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Room(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return f'Nombre de foro {self.name}'

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

    def __str__(self):
        return f'Mensaje de {self.user} en foro {self.room}'

    