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
		'form': form,
		"errmsg":""
	}

	if request.method == 'POST':
		visitor_id = request.POST['visitor_id']
		visitor_name = request.POST['visitor_name']
		Alumni_id = request.POST['Alumni_id']
		phone_num = request.POST['phone_num']
		email = request.POST['email']

		home_address = request.POST['home_address_city'] + request.POST['home_address_area'] + request.POST['home_address']
		connect_address = request.POST['mail_address_city'] + request.POST['mail_address_area'] + request.POST['mail_address']

		try:
			user_email = visitor.objects.filter(email = email)
			print(user_email)

		except Exception as e:
			user_email = None

		if user_email:
			context = {
				'form': form,
				"errmsg":"*郵箱已經被使用"
			}
			return render(request, 'sign_in.html', context)

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

def admin_index(request):
	return render(request, 'admin_index.html')

def register(request):
	form = RegisterForm()
	context = {
		'form': form,
		'person_status': ""
	}

	if request.method == 'POST':
		visitor_id = request.POST['visitor_id']
		Alumni_id = request.POST['Alumni_id']
		if Alumni_id == "":
			person = visitor.objects.filter(visitor_id = visitor_id).first()
		elif visitor_id == "":
			person = visitor.objects.filter(Alumni_id = Alumni_id).first()
		
		if person == None or person.isactivate == False:
			context = {
				'form': form,
				'person_status': '查無註冊資料'
			}
			return render(request, 'register.html', context)
		else:
			data = access.objects.filter(visitor_id = person.visitor_id, return_date__isnull = True).first()
			if data == None:
				print(person.visitor_id)
				request.session['visitor_id'] = person.visitor_id
				return redirect('step2/', visitor_id = person.visitor_id)
			else:
				context = {
					'form': form,
					'person_status': '此訪客已借用訪客證，尚未歸還'
				}
				return render(request, 'register.html', context)
	return render(request, 'register.html', context)

def register_step2(request):
	visitor_id = request.session.get('visitor_id', default="")
	person = visitor.objects.get(visitor_id = visitor_id)
	context = {
		'person': person,
	}
	if request.method == 'POST':
		visitor_card = request.POST['visitor_card']
		#data = access.objects.create(place = place, visitor_id = person, Alumni_id = person.Alumni_id, visitor_card = visitor_card)
		# data.save()
	return render(request, 'register_2.html', context)

def detail(request, pk):
	data = access.objects.get(pk = pk)
	context = {
		'data': data
	}
	return render(request, 'detail.html', context)

def Return(request):
	context = {
		'errmsg': ''
	}

	if request.method == 'POST':
		visitor_card = request.POST.get('visitor_card', '')
		data = access.objects.filter(visitor_card = visitor_card, return_date__isnull = True).first()

		if data is None:
			context = {
				'errmsg': '*查無借用資料，請再次輸入'
			}
			return render(request, 'return.html', context)
		else:
			data = data
			data.return_date = datetime.now()
			print(data.return_date)
			data.save()
			return redirect(str(data.pk) + '/detail', pk = data.pk)
	return render(request, 'return.html', context)

def send_revise_email(request):
	if request.method == 'POST':
		visitor_id = request.POST['visitor_id']

		try:
			user = visitor.objects.filter(visitor_id = visitor_id)
		except Exception as e:
			user = None

		if user:
			# 寄送email
			token = visitor().generate_activate_token().decode('utf-8')
			user = user.first()
			user.token = token
			user.save()

			subject, from_email, to = '資料修改', 'blackcat.in.the.midnight@gmail.com', user.email
			text_content = 'This is an important message.'
			html_content = '<p><a href="http://127.0.0.1:8000/revise_database/?token=' + token + '">修改</a></p>'
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

	return render(request, 'send_revise_email.html')

def revise_database(request):
	token = request.GET['token']
	result, user = visitor.check_activate_token(token)
	if result:
		print(result)
		form = SignInForm()

		count = 0
		home = []
		for i in range(len(user.home_address)):
			if user.home_address[i] in ['縣','市','區','鄉','鎮']:
				home.append(user.home_address[count:i+1])
				count = i+1
		home.append(user.home_address[count:i+1])

		count = 0
		connect = []
		for i in range(len(user.connect_address)):
			if user.connect_address[i] in ['縣','市','區','鄉','鎮']:
				connect.append(user.connect_address[count:i+1])
				count = i+1
		connect.append(user.connect_address[count:i+1])

		context = {
			'form': form,
			'user': user,
			'home_city': home[0],
			'home_area': home[1],
			'home_road': home[2],
			'connect_city': connect[0],
			'connect_area': connect[1],
			'connect_road': connect[2]
		}
		return render(request, 'revise_database.html', context)
	else:
		return HttpResponse("驗證失敗")