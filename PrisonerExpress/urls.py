from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from PrisonerExpress import views
from PrisonerExpress import prison_views
from PrisonerExpress import program_views

prison_patterns=patterns(
    '',
    url(regex=r'^$',
        view=prison_views.index,
        name='prison_list'),
    url(regex=r'^(?P<prison_id>\d+)/$',
        view=prison_views.details,
        name='prison_details'),
    url(regex=r'^create$',
        view=prison_views.create,
        name='prison_create'),
    url(regex=r'^(?P<prison_id>\d+)/edit$',
        view=prison_views.edit,
        name='prison_edit'),
    )

program_patterns=patterns(
    '',
    url(regex=r'^$',
        view=program_views.index,
        name='program_list'),
    url(regex=r'^(?P<program_id>\d+)/$',
        view=program_views.details,
        name='program_details'),
    url(regex=r'^create$',
        view=program_views.create,
        name='program_create'),
    url(regex=r'^(?P<program_id>\d+)/edit$',
        view=program_views.edit,
        name='program_edit'),
    )



urlpatterns= patterns(
    '',
    url(regex=r'^$',
        view=TemplateView.as_view(template_name="foundation/index.html"),
        name="foundation_index"),
   	url(r'^program/', include(program_patterns)), 
	url(r'^prison/', include(prison_patterns)), 
)


