# -*- coding: utf-8 -*-
from django import forms
from django.db.models.enums import Choices
from django.forms import fields
from django.core.exceptions import ValidationError
from .models import visitor, access

class SignInForm(forms.ModelForm):
	class Meta:
		# 指定使用的model
		model = visitor
		# 設定要顯示的欄位
		fields = ('visitor_id', 'visitor_name', 'phone_num','email', 'Alumni_id')
		
		# 設定表單的顯示外觀
		widgets = {
			'visitor_id': forms.TextInput(attrs={'style': 'background-color:white'}),
			'email': forms.TextInput(attrs={'placeholder': "請填常用信箱避免接收不到驗證信件"})
		}

		#設定表單的顯示欄位名稱
		labels = {
			'visitor_id': '身分證字號',
			'Alumni_id': '校友證字號',
			'visitor_name': '名稱',
			'phone_num': '連絡電話',
			'email': '電子郵件',	
		}
		
# 換證
class RegisterForm(forms.ModelForm):
	class Meta:
		model = access
		fields = ('place', 'visitor_id', 'Alumni_id', 'visitor_card')
		widgets = {
			'visitor_id': forms.TextInput(),
		}
		labels = {
			'place': '登記地點',
			'visitor_card': '訪客證號'
		}

