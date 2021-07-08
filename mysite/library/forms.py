from django import forms
from django.forms import fields
from .models import visitor, access

def email_check(email):
	pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
	return re.match(pattern, email)

class SignInForm(forms.ModelForm):

	class Meta:
		# 指定使用的model
		model = visitor
		# 設定要顯示的欄位
		fields = ('visitor_id', 'visitor_name', 'phone_num','email', 'Alumni_id')
		
		# 設定表單的顯示外觀
		# widgets = {
		#     'name': forms.TextInput(attrs={'class': 'form-control'}),
		#     'price': forms.NumberInput(attrs={'class': 'form-control'})
		# }

		#設定表單的顯示欄位名稱

		labels = {
			'visitor_id': '身分證字號',
			'Alumni_id': '校友證字號',
			'visitor_name': '名稱',
			'phone_num': '連絡電話',
			'email': '電子郵件',	
		}

# 換證
class Register(forms.ModelForm):
	class Meta:
		model = access
		fields = ('place', 'visitor_id', 'Alumni_id', 'visitor_card')
		labels = {
			'place': '登記地點',
			'visitor_id': '身分證字號',
			'Alumni_id': '校友證號',
			'visitor_card': '訪客證號'
		}