from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from PrisonerExpress import views
from PrisonerExpress import prison_views

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


urlpatterns= patterns(
    '',
    url(regex=r'^$',
        view=TemplateView.as_view(template_name="foundation/index.html"),
        name="foundation_index"),
    url(r'^prison/', include(prison_patterns)), 
)


