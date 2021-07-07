from django import forms
from .models import visitor, access

def email_check(email):
	pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
	return re.match(pattern, email)

class SignInForm(forms.ModelForm):

	class Meta:
		# 指定使用的model
		model = visitor
		# 設定要顯示的欄位
		fields = ('visitor_id', 'visitor_name', 'email', 'cellphone', 'tellphone', 'Alumni_id', 'home_address', 'connect_address')
		
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
			'email': '電子郵件',
			'cellphone': '手機號碼',
			'tellphone': '電話號碼',
			'home_address': '住家地址',
			'connect_address': '通訊地址'		
		}