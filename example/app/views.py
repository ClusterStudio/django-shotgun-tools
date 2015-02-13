# code: utf-8

from django.views.generic import TemplateView


class IndexView(TemplateView):
	template_name = "app/index.html"

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		project_id = int(self.request.GET.get('project', '2618'))
		versions = self.request.shotgun.findLazy("Version",
			[['project','is', {'type':'Project', 'id':project_id}]],
			order=[{'field_name':'created_at', 'direction':'desc'}],
			limit=10)
		context['versions_list'] = versions
		return context

index_view = IndexView.as_view()
