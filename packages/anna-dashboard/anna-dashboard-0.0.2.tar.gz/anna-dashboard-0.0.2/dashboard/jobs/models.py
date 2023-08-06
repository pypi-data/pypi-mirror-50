from django.db import models


class Job(models.Model):
	job_id = models.IntegerField(blank=True, null=True, default=None)
	driver = models.CharField(max_length=256)
	site = models.CharField(max_length=256)
	status = models.CharField(max_length=256, blank=True)
	tag = models.CharField(max_length=256, blank=True)
	container = models.CharField(max_length=256, blank=True)
	log = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True)
