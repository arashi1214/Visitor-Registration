from django.conf import settings
from django.db import models
from django.db.models.base import ModelState
from django.utils import timezone

# Token 產生測試
from django.contrib.auth.hashers import make_password
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired
from itsdangerous import BadSignature,SignatureExpired

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
    isactivate = models.BooleanField(default=False)
    token = models.CharField(max_length = 500, default="")

        #生成token
    def generate_activate_token(self, expires_in=360):
        s = Serializer(settings.SECRET_KEY, expires_in)
        return s.dumps({'visitor_id': self.visitor_id})

    @staticmethod
    def check_activate_token(token):
        # s = Serializer(settings.SECRET_KEY)
        # try:
        #     data = s.loads(token)
        # except BadSignature:
        #     return '無效的驗證碼'
        # except SignatureExpired:
        #     return '驗證碼已過期'
        user = visitor.objects.filter(token=token).first()
        if not user:
            return '該帳號不存在'
        if not user.is_acitve:
            user.is_acitve = True
            user.save()
        return '驗證成功'

# 進出資料表
class access(models.Model):
    place_choices = (
        ('濟時樓', '濟時樓'),
        ('公博樓', '公博樓'),
        ('公博樓','國璽樓')
    )
    visitor_id = models.ForeignKey('visitor', on_delete = models.CASCADE)
    Alumni_id = models.CharField(max_length = 9, blank = True)
    visitor_card = models.CharField(max_length = 10)
    place = models.CharField(max_length = 10, choices=place_choices)
    lend_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(blank=True, null=True)


# 本機測試時候更改model資料後，要告至django的寫法
# manage.py makemigrations
# manage.py migrate