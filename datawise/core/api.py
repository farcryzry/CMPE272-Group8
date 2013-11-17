from tastypie.resources import ModelResource

from tastypie import fields

from core.models import Result

class ResultResource(ModelResource):
    class Meta:
        queryset = Result.objects.all()
        include_resource_uri = True
        resource_name = 'result'