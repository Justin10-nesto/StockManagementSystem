import datetime
from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.

class OtpCode(models.Model):
    code = models.CharField(max_length=100)
    is_used = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_status(self):
        date = datetime.datetime(self.date_created.year, self.date_created.month, self.date_created.day, self.date_created.hour +3, self.date_created.minute, self.date_created.second)

        if date > self.date_created:
            return 'Valid'
        else:
            return 'Invalid'

    class Meta:
        verbose_name = "OtpCode"
        db_table = "OtpCode"
