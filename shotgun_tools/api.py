# coding: utf-8
import re

from tastypie import fields
from tastypie.resources import Resource, Bundle
from tastypie.exceptions import NotFound
import ShotgunORM

from .settings import SHOTGUN_ENTITY_TYPES
from .utils import get_sg_connection

class ShotgunEntityResource(Resource):
    # Just like a Django ``Form`` or ``Model``, we're defining all the
    # fields we're going to handle with the API here.
    id = fields.IntegerField(attribute='id')
    #type = fields.CharField(attribute='type')

    class Meta:
        pass
        # resource_name = 'entity'
        #object_class = ShotgunEntity
        # authorization = Authorization()

    @property
    def _sg(self):
        if not hasattr(self, "_shotgun"):
            self._shotgun = get_sg_connection()
        return self._shotgun

    # The following methods will need overriding regardless of your
    # data source.
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):
        fields_list = self._schema.fieldInfos().keys()
        results = self._sg.findLazy(self._entity_type, [], fields_list)
        return results

    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        fields_list = self._schema.fieldInfos().keys()
        obj = self._sg.findOne(
            self._entity_type, [["id", "is", int(kwargs['pk'])]], fields_list)
        if not obj or not obj.id:
            raise NotFound("Object not found")
        return obj

    def obj_create(self, bundle, **kwargs):
        bundle.obj = ShotgunEntity(initial=kwargs)
        bundle = self.full_hydrate(bundle)
        new_message = self._sg.create(
            self._entity_type, bundle.obj.to_dict())
        return bundle

    def obj_update(self, bundle, **kwargs):
        return self.obj_create(bundle, **kwargs)

    def obj_delete_list(self, bundle, **kwargs):
        bucket = self._bucket()

        for key in bucket.get_keys():
            obj = bucket.get(key)
            obj.delete()

    def obj_delete(self, bundle, **kwargs):
        obj = self._sg.findOne(self._entity_type, [["id", "is", kwargs['pk']]])
        obj.delete()

    def rollback(self, bundles):
        pass


def cammel_case_to_slug(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


sg = get_sg_connection()

def shotgun_entity_resource_factory(entity_type):
    schema = sg.schema().entityInfo(entity_type)

    class EntityResource(ShotgunEntityResource):
        _entity_type = entity_type
        _schema = schema

        class Meta(ShotgunEntityResource.Meta):
            resource_name = cammel_case_to_slug(entity_type)

    if schema:
        for field_name in sg.defaultEntityQueryFields(entity_type):
            field_info = schema.fieldInfos()[field_name]
            return_type = field_info.returnType()
            resource_field = dehydrate_method = None
            # RETURN_TYPE_CHECKBOX = 0
            if return_type == ShotgunORM.SgField.RETURN_TYPE_CHECKBOX:
                resource_field = fields.BooleanField(attribute=field_name, null=True)
            # RETURN_TYPE_DATE = 3
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_DATE:
                resource_field = fields.DateField(attribute=field_name, null=True)
            # RETURN_TYPE_DATE_TIME = 4
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_DATE_TIME:
                resource_field = fields.DateTimeField(attribute=field_name, null=True)
            # RETURN_TYPE_FLOAT = 6
            elif return_type ==ShotgunORM.SgField.RETURN_TYPE_FLOAT:
                resource_field = fields.FloatField(attribute=field_name, null=True)
            # RETURN_TYPE_INT = 8
            elif return_type ==ShotgunORM.SgField.RETURN_TYPE_INT:
                resource_field = fields.IntegerField(attribute=field_name, null=True)
            # RETURN_TYPE_URL = 16
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_URL:
                resource_field = fields.DictField(attribute=field_name, null=True)
            # RETURN_TYPE_TEXT = 15
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_TEXT:
                resource_field = fields.CharField(attribute=field_name, null=True)
            # RETURN_TYPE_ENTITY = 5
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_ENTITY:
                resource_field = fields.IntegerField(attribute=field_name, null=True)
                #def dehydrate_method_factory(field_name):
                #    def dehydrate_method(self, bundle):
                #        # assert False, bundle.data.keys()
                #        return bundle.data[field_name]
                #    return dehydrate_method
                #setattr(EntityResource, "dehydrate_%s" % field_name, dehydrate_method_factory(field_name))
            # RETURN_TYPE_MULTI_ENTITY = 10
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_MULTI_ENTITY:
                pass
                #resource_field = fields.CharField(attribute=field_name, null=True)
            # RETURN_TYPE_SERIALIZABLE = 11
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_SERIALIZABLE:
                resource_field = fields.DictField(attribute=field_name, null=True)
            # RETURN_TYPE_TAG_LIST = 14
            elif return_type == ShotgunORM.SgField.RETURN_TYPE_TAG_LIST:
                resource_field = fields.ListField(attribute=field_name, null=True)
            # RETURN_TYPE_LIST = 9
            # RETURN_TYPE_STATUS_LIST = 12
            # RETURN_TYPE_SUMMARY = 13
            # RETURN_TYPE_COLOR = 1
            # RETURN_TYPE_COLOR2 = 2
            # RETURN_TYPE_IMAGE = 7
            # RETURN_TYPE_UNSUPPORTED = -1
            elif return_type != ShotgunORM.SgField.RETURN_TYPE_UNSUPPORTED:
                resource_field = fields.CharField(attribute=field_name, null=True)

            if resource_field:
                EntityResource.base_fields[field_name] = resource_field

    return EntityResource


def shotgun_rest_api_factory(entity_types=SHOTGUN_ENTITY_TYPES):
    from tastypie.api import Api
    sg_api = Api(api_name='v3')
    for entity_type in entity_types:
        sg_api.register(shotgun_entity_resource_factory(entity_type)())
    return sg_api
