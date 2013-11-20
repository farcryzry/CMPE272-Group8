from django.conf.urls import patterns, url, include

from core import views
from django.views.generic import TemplateView

from core.api import ResultResource

result_resource = ResultResource()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='core/index.html'), name='index'),
    url(r'^index/$', TemplateView.as_view(template_name='core/index.html'), name='index'),
    url(r'^mood/$', TemplateView.as_view(template_name='core/mood.html'), name='calendar'),
    url(r'^correlation/$', TemplateView.as_view(template_name='core/correlation.html'), name='correlation'),
    url(r'^planet/$', TemplateView.as_view(template_name='core/planet.html'), name='matrix'),

    url(r'^api/', include(result_resource.urls)),
)