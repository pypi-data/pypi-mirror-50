from django.http import HttpResponse
from django.template import loader


def index(request):
	template = loader.get_template('unittests/index.html')
	return HttpResponse(template.render({}, request))


def switch_to(request):
	template = loader.get_template('unittests/switch_to.html')
	return HttpResponse(template.render({}, request))
