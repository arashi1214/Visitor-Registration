from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from .models import visitor, access
from .forms import SignInForm, RegisterForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
# from utils.token import Token
# from django.core.mail import send_mail

# token_confirm = Token(SECRET_KEY)

# class Token():
# 	def __init__(self,security_key):
# 		self.security_key = security_key
# 		self.salt = base64.encodestring(security_key)
# 	def generate_validate_token(self,username):
# 		serializer = utsr(self.security_key)
# 		return serializer.dumps(username,self.salt)
# 	def confirm_validate_token(self,token,expiration=3600):
# 		serializer = utsr(self.security_key)
# 		return serializer.loads(token,
# 		salt=self.salt,
# 		max_age=expiration) 

def sign_in(request):

	form = SignInForm()
	context = {
		'form': form
	}

	if request.method == 'POST':
		visitor_id = request.POST['visitor_id']
		visitor_name = request.POST['visitor_name']
		Alumni_id = request.POST['Alumni_id']
		phone_num = request.POST['phone_num']
		email = request.POST['email']

		home_address = request.POST['home_address_city'] + request.POST['home_address_area'] + request.POST['home_address']
		connect_address = request.POST['mail_address_city'] + request.POST['mail_address_area'] + request.POST['mail_address']

		data = visitor.objects.create(visitor_id=visitor_id, visitor_name=visitor_name, Alumni_id=Alumni_id, phone_num=phone_num, email=email, home_address=home_address, connect_address=connect_address)
		data.save()


	return render(request, 'sign_in.html', context)

def register(request):
	form = RegisterForm()
	
	context = {
		'form': form
	}

	if request.method == 'POST':
		place = request.POST['place']
		visitor_id = request.POST['visitor_id']
		Alumni_id = request.POST['Alumni_id']
		visitor_card = request.POST['visitor_card']

		id = visitor.objects.filter(visitor_id = visitor_id).first()

		data = access.objects.create(place = place, visitor_id = id, Alumni_id = Alumni_id, visitor_card = visitor_card)
		data.save()
	
	return render(request, 'register.html', context)

def Return(request):
	if request.method == 'POST':
		visitor_card = request.POST['visitor_card']
		
		data = access.objects.filter(visitor_card = visitor_card, return_date__isnull = True).first()
		data.return_date = datetime.now()
		data.save()

	return render(request, 'return.html')