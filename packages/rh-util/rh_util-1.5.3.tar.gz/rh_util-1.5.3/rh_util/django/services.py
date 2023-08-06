from django.utils import timezone
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super().__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
    
                
class BaseDao:
    __queryset = None
    
    def save(self, objeto):
        objeto.save()
    
    @property
    def queryset(self):
        return self.__queryset
    
    @queryset.setter
    def queryset(self, queryset):
        self.__queryset = queryset
    
    def get_all(self):
        return self.queryset.all()
    
    def get_all_by_fields(self, **fields):
        return self.queryset.filter(**fields)


class BaseModelViewSet(ModelViewSet):
    
    def perform_create(self, serializer):
        fields = {}
        if hasattr(serializer.Meta.model, 'user'):
            fields['user'] = self.request.user
        serializer.save(**fields)
    
    def perform_update(self, serializer):
        fields = {}
        if hasattr(serializer.Meta.model, 'user'):
            fields['user'] = self.request.user
        if hasattr(serializer.Meta.model, 'data_alt'):
            fields['data_alt'] = timezone.now()
        serializer.save(**fields)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, 'ativo'):
            instance.ativo = 0
            if hasattr(instance, 'data_fim'):
                instance.data_fim = timezone.now()
            instance.save()
        else:
            self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
