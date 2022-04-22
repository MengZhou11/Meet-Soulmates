from django.db import models

# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_desc = models.CharField(max_length=200)
    create_date = models.DateTimeField(blank=True,null=True)
    update_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.project_name

