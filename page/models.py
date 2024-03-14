from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.IntegerField()
    server_id = models.IntegerField()
    

class Server(models.Model):
    user_id = models.IntegerField()
    rol_id = models.IntegerField()
    xp = models.IntegerField()
