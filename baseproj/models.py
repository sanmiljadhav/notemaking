from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    note_title = models.CharField(max_length=100)
    note_description = models.TextField()
    class Meta:
        db_table = "notes"





    
