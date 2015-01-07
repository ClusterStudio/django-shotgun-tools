# coding: utf-8
from .utils import get_sg_connection


class ShotgunMiddleware(object):
	def process_request(self, request):
		setattr(request, 'shotgun', get_sg_connection())