from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from .models import visitor, access
from .forms import SignInForm, RegisterForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.http import HttpResponse

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

		# 產生token
		token = visitor().generate_activate_token().decode('utf-8')
		data = visitor.objects.create(visitor_id=visitor_id, visitor_name=visitor_name, Alumni_id=Alumni_id, phone_num=phone_num, email=email, home_address=home_address, connect_address=connect_address, token=token)
		
		data.save()

		# 寄送email
		subject, from_email, to = '信箱驗證', 'blackcat.in.the.midnight@gmail.com', email
		text_content = 'This is an important message.'
		html_content = '<p><a href="http://127.0.0.1:8000/activate/?token=' + token + '">驗證</a></p>'
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

	return render(request, 'sign_in.html', context)


def activate(request):
    token = request.GET['token']
    result = visitor.check_activate_token(token)
    return HttpResponse(result)

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