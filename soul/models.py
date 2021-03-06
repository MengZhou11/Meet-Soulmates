from django.db import models

# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    create_date = models.DateTimeField(blank=True,null=True)
    update_date = models.DateTimeField(blank=True,null=True)
    EXT = models.CharField(max_length=100)
    EST = models.CharField(max_length=100)
    AGR = models.CharField(max_length=100)
    CSN = models.CharField(max_length=100)
    OPN = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Blog(models.Model):
    user = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    create_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.subject

