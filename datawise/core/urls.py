from django.conf.urls import patterns, url, include

from core import views
from django.views.generic import TemplateView

from core.api import ResultResource

result_resource = ResultResource()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='core/index.html'), name='index'),
    url(r'^index/$', TemplateView.as_view(template_name='core/index.html'), name='index'),
    url(r'^calendar/$', TemplateView.as_view(template_name='core/calendar.html'), name='calendar'),
    url(r'^stats/$', TemplateView.as_view(template_name='core/stats.html'), name='stats'),
    url(r'^form/$', TemplateView.as_view(template_name='core/form.html'), name='form'),
    url(r'^tables/$', TemplateView.as_view(template_name='core/tables.html'), name='tables'),
    url(r'^buttons/$', TemplateView.as_view(template_name='core/buttons.html'), name='buttons'),
    url(r'^interface/$', TemplateView.as_view(template_name='core/interface.html'), name='interface'),
    url(r'^login/$', TemplateView.as_view(template_name='core/login.html'), name='login'),
    url(r'^editors/$', TemplateView.as_view(template_name='core/editors.html'), name='editors'),

    url(r'^api/', include(result_resource.urls)),
)