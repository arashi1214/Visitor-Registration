from django.shortcuts import render, redirect, get_object_or_404

from .models import visitor, access
from .forms import SignInForm

def sign_in(request):

	form = SignInForm()
	context = {
		'form': form
	}

	if request.method == 'POST':
		pass

	return render(request, 'sign_in.html', context)