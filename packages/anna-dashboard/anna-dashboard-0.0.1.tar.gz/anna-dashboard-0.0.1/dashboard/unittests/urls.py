from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('switchto', views.switch_to, name='switch_to'),
]