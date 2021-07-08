from django.conf import settings
from django.db import models
from django.db.models.base import ModelState
from django.utils import timezone

# 外賓資料表
class visitor(models.Model):
    visitor_name = models.CharField(max_length = 20)
    visitor_id = models.CharField(max_length = 10, primary_key = True)
    Alumni_id = models.CharField(max_length = 9, blank = True)
    phone_num = models.CharField(max_length = 15)
    email = models.EmailField()
    home_address = models.CharField(max_length = 50)
    connect_address = models.CharField(max_length = 50)
    created_date = models.DateTimeField(default=timezone.now)

# 進出資料表
class access(models.Model):
    visitor_id = models.ForeignKey('visitor', on_delete = models.CASCADE)
    Alumni_id = models.CharField(max_length = 9, blank = True)
    visitor_card = models.CharField(max_length = 10)
    place = models.CharField(max_length = 10)
    lend_date = models.DateTimeField(default=timezone.now)
    
    def return_time(self):
        self.return_date = models.DateTimeField(blank=True, null=True)
        self.save()


# 本機測試時候更改model資料後，要告至django的寫法
# manage.py makemigrations
# manage.py migrate