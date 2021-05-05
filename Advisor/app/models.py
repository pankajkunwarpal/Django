from django.db import models
from datetime import datetime


# username: admin1
# pswd: qaws1324

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(instance, filename)
    return 'app/static/MEDIA/user_{0}/{1}/{2}'.format(instance.userid, datetime.now().date().strftime('%Y/%m/%d'),filename)

class Advisor(models.Model):
    userid = models.IntegerField(blank=False, default=1)
    name = models.CharField(max_length=50)
    media = models.FileField(upload_to=user_directory_path)

class Calls(models.Model):
    userid = models.IntegerField(blank=False, default=1)
    date = models.DateTimeField(default=datetime.now().strftime('%Y %B %d %H:%M'))
    advisor = models.IntegerField(blank=False, default=1)

 
