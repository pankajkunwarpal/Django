from django.db import models

# Create your models here.
# Username:  pankaj
# password:  qazx90-=

class Directory(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    date = models.DateTimeField()
    booked_by = models.CharField(max_length=50, default='self')

    class Meta:
        db_table = "directory"

    def __str__(self):
        return self.name.capitalize()

