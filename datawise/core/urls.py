from django.conf.urls import patterns, url, include

from core import views
from django.views.generic import TemplateView

from core.api import ResultResource

result_resource = ResultResource()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='core/index.html'), name='index'),
    url(r'^index/$', TemplateView.as_view(template_name='core/index.html'), name='index'),
    url(r'^mood/$', TemplateView.as_view(template_name='core/mood.html'), name='mood'),
    url(r'^correlation/$', TemplateView.as_view(template_name='core/correlation.html'), name='correlation'),
    url(r'^planet/$', TemplateView.as_view(template_name='core/planet.html'), name='planet'),
    url(r'^trends/$', TemplateView.as_view(template_name='core/trends.html'), name='trends'),
	url(r'^hottechs/$', TemplateView.as_view(template_name='core/hottechs.html'), name='hottechs'),

    url(r'^api/', include(result_resource.urls)),
)