from django.shortcuts import render, redirect, get_object_or_404

from .models import visitor, access
from .forms import SignInForm

import time

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

		print(visitor_id)
		print(visitor_name)
		print(Alumni_id)
		print(phone_num)
		print(email)
		print(home_address)
		print(connect_address)
		print(time.localtime())

		data = visitor.objects.create(visitor_id=visitor_id, visitor_name=visitor_name, Alumni_id=Alumni_id, phone_num=phone_num, email=email, home_address=home_address, connect_address=connect_address)
		data.save()

	return render(request, 'sign_in.html', context)