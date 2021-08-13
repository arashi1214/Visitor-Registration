"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url

from library.views import sign_in, register, register_step2, Return, activate, detail, send_revise_email, revise_database, admin_index, user_index, report

urlpatterns = [
    url(r'^$', user_index),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('sign_in/', sign_in),
    path('admin_index/', admin_index),
    path('user_index/', user_index),
    path('register/', register),
    re_path(r'register/step2/', register_step2),
    path('return/', Return),
    path('report/', report),
    path(r'activate/', activate),
    path('send_revise_email/', send_revise_email),
    path(r'revise_database/', revise_database),
    re_path(r'^return/(?P<pk>[0-9]+)/detail/$', detail)
]