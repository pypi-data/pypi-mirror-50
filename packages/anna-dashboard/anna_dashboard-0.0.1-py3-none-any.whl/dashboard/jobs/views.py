import re
import json
import hashlib

from django.http import HttpResponse
from django.template import loader

from basicauth.decorators import basic_auth_required

from anna_client.client import Client


@basic_auth_required
def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render({}, request))


@basic_auth_required
def search(request):
	client = Client(endpoint='http://localhost:5000/graphql')
	query = {}
	for key, val in dict(request.GET).items():
		if key == 'hash':
			continue
		if isinstance(val, list):
			query[str(key).replace('[]', '') + '_in'] = val
		else:
			query[str(key).replace('[]', '')] = val
	response = client.get_jobs(where=query, fields=('id','status','driver','site','worker','container'))
	response_hash = hashlib.sha256(bytes(str(response).encode())).hexdigest()
	if 'hash' in query:
		if len(query['hash']) > 0 and query['hash'][0] == response_hash:
			return HttpResponse()
		del query['hash']
	jobs = []
	for job in response:
		jobs.append({
			'tag': job['container'], 'driver': job['driver'], 'site': job['site'], 'status': job['status'],
			'worker': job['worker']})
	return HttpResponse(json.dumps({'jobs': jobs, 'hash': response_hash}), content_type='application/json')
