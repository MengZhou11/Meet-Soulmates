from django.db import models

# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    create_date = models.DateTimeField(blank=True,null=True)
    update_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

