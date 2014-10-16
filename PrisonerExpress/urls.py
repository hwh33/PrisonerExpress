from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from PrisonerExpress import views
from PrisonerExpress import prison_views
from PrisonerExpress import program_views
from PrisonerExpress import prisoner_views
from PrisonerExpress import letter_views
from prisoner_views import PrisonerList, PrisonerDetail, PrisonerIndex
from program_views import ProgramDetails, ProgramIndex
from prison_views import PrisonIndex

prison_patterns=patterns(
    '',
    url(regex=r'^$',
        view=PrisonIndex.as_view(),
        name="prison_index"),
    url(regex=r'^list',
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
    url(r'^$',
        ProgramIndex.as_view(),
        name="program_index"),
    url(regex=r'^list',
        view=program_views.index,
        name='program_list'),
    url(r'^(?P<pk>\d+)/$',
        ProgramDetails.as_view(),
        name='program_details'),
    url(regex=r'^create$',
        view=program_views.create,
        name='program_create'),
    url(regex=r'^(?P<program_id>\d+)/edit$',
        view=program_views.edit,
        name='program_edit'),
    )

prisoner_patterns=patterns(
    '',
    url(r'^$',
        PrisonerIndex.as_view(),
        name="prisoner_index"),
    url(r'^list',
        PrisonerList.as_view(),
        name="prisoner_list"),
    url(regex=r'^create$',
        view=prisoner_views.create,
        name='prisoner_create'),
    url('^(?P<pk>\d+)/$',
        PrisonerDetail.as_view(),
        name='prisoner_details'),
    )



urlpatterns= patterns(
    '',
    url(regex=r'^$',
        view=TemplateView.as_view(template_name="index.html"),
        name="index"),
    url(r'^program/', include(program_patterns)), 
    url(r'^prison/', include(prison_patterns)),
    url(r'^prisoner/', include(prisoner_patterns)),
    url(regex=r'^letters/new$',
        view=letter_views.new,
        name='new_letter')
)

