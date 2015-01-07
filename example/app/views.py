# code: utf-8

from django.views.generic import TemplateView
from shotgun_tools.views.decorators import with_shotgun


class IndexView(TemplateView):
	template_name = "app/index.html"

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		project_id = int(self.request.GET.get('project', '2618'))
		versions = self.request.shotgun.find("Version",
			[['project','is', {'type':'Project', 'id':project_id}]],
			order=[{'field_name':'created_at', 'direction':'desc'}],
			limit=10, lazy=True)
		context['versions_list'] = versions
		return context

index_view = with_shotgun(IndexView.as_view())
