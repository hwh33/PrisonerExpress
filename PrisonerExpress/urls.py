from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView
from PrisonerExpress import prison_views, program_views, prisoner_views, letter_views, user_views, tests, index_view, admin_views
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
    url(regex=r'^(?P<program_id>\d+)/new_iteration$',
        view=program_views.create_iteration,
        name="iteration_create"),
    url(regex=r'^(?P<program_id>\d+)/iterations',
        view=program_views.list_iterations,
        name="list_iterations"),
    url(regex=r'^iteration/(?P<iteration_id>\d+)',
        view=program_views.get_iteration_details,
        name="iteration_details"),
    url(regex=r'^(?P<program_id>\d+)/two_col_labels$',
        view=program_views.mail,
        name='program_two_col_labels'),
    url(regex=r'^(?P<program_id>\d+)/three_col_labels$',
        view=program_views.mail,
        name='program_three_col_labels'),
    url(regex=r'^(?P<program_id>\d+)/letter_input$',
        view=program_views.input,
        name='program_input'),
    url(regex=r'^(?P<iteration_id>\d+)/new_subprogram',
        view=program_views.create_subprogram,
        name='subprogram_create')
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
    url(regex=r'^edit/(?P<prisoner_id>\w+)',
        view=prisoner_views.edit,
        name='prisoner_edit'),
    url(regex=r'^query',
        view=prisoner_views.query,
        name='prisoner_query'),
    url('^(?P<pk>\w+)/$',
        PrisonerDetail.as_view(),
        name='prisoner_details'),
    )


user_patterns=patterns(
    '',
    url(r'^login$',
        user_views.user_login,
        name='user_login'),
    url(r'^logout$',
        user_views.user_logout,
        name='user_logout'),
    url(r'^register$',
        user_views.user_register,
        name='user_register'),
    url(r'^user_ctrl',
        user_views.user_ctrl,
        name='user_ctrl'),
    url(regex=r'^profile$',
        view=user_views.user_profile,
        name='user_profile'),
    url(regex=r'^edit$',
        view=user_views.user_edit,
        name='user_edit',)
)
letter_patterns=patterns(
    '',
    url(r'^new$',
        view=letter_views.new,
        name='new_letter'),
    url(r'^(?P<letter_id>\d+)/edit$',
        view=letter_views.edit,
        name='letter_edit'),
    url(regex=r'^list',
        view=letter_views.index,
        name='letter_list'),

)
urlpatterns= patterns(
    '',
    url(regex=r'^$',
        view=index_view.public_page,
        name="index"),
    url(regex=r'^settings$',
        view=admin_views.settings,
        name="admin_settings"),
    url(r'^program/', include(program_patterns)),
    url(r'^prison/', include(prison_patterns)),
    url(r'^prisoner/', include(prisoner_patterns)),
    url(r'^letters/',include(letter_patterns)),
    url(r'^user/',include(user_patterns)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
)
