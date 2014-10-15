from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from PrisonerExpress import views

urlpatterns= patterns('',
	#url(r'^$',views.index,name='index'),
	url(regex=r'^$',
        view=TemplateView.as_view(template_name="foundation/index.html"),
        name="foundation_index"),
)


