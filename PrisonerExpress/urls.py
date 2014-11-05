from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView
from PrisonerExpress import prison_views, program_views, prisoner_views, letter_views, user_views, tests
from prisoner_views import PrisonerList, PrisonerDetail, PrisonerIndex
from program_views import ProgramDetails, ProgramIndex
from prison_views import PrisonIndex, PrisonDetails, PrisonList


prison_patterns=patterns(
    '',
    url(regex=r'^$',
        view=PrisonIndex.as_view(),
        name="prison_index"),
    url(regex=r'^list',
        view=PrisonList.as_view(),
        name='prison_list'),
    url(regex=r'^(?P<pk>\d+)/$',
        view=PrisonDetails.as_view(),
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
        name='program_details', ),
    url(regex=r'^create$',
        view=program_views.create,
        name='program_create'),
    url(regex=r'^(?P<program_id>\d+)/edit$',
        view=program_views.edit,
        name='program_edit'),
     url(regex=r'^(?P<program_id>\d+)/mail$',
        view=program_views.mail,
        name='program_mail'),
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
    url(regex=r'^search',
        view=prisoner_views.search,
        name='prisoner_search'),
    url('^(?P<pk>\w+)/$',
        PrisonerDetail.as_view(),
        name='prisoner_details'),
    )


user_patterns=patterns(
    '',
    url(r'^login$',
        user_views.user_login,
        name='login'),
    url(r'^logout$',
        user_views.user_logout,
        name='logout'),
    url(r'^register$',
        user_views.user_register,
        name='register'),
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
        name='new_letter'),
    url(r'^user/',include(user_patterns)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'fast_input',tests.input),
)
