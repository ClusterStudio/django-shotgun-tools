# coding: utf-8
import re

from tastypie import fields
from tastypie.resources import Resource, Bundle

<<<<<<< HEAD
#from shotgun_api3 import Shoitgun
=======
>>>>>>> 3b90238a56f1c0c61df6003446d86c569b079845
import ShotgunORM
from .settings import SHOTGUN_SERVER, SHOTGUN_SCRIPT_NAME, SHOTGUN_SCRIPT_KEY, \
    SHOTGUN_ENTITY_TYPES

# We need a generic object to shove data in/get data from.
# Shotgun generally just tosses around dictionaries, so we'll lightly
# wrap that.
class ShotgunEntity(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return getattr(self._data, name)

    def __setattr__(self, name, value):
        setattr(self.__dict__['_data'], name, value)

    def to_dict(self):
        return self._data.to_dict()


class LazyFind(object):
    def __init__(self, shotgun, entity_type, filters, fields):
        self.__dict__['_data'] = []
        self._entity_type_type = entity_type
        self.filters = filters
        self.fields = fields
        self.shotgun = shotgun

    def __len__(self):
        if not hasattr(self, '_summaries'):
            self._summaries = self.shotgun.summarize(
                entity_type=self._entity_type_type,
                filters = [],
                summary_fields=[{'field':'id', 'type':'count'}]
            ).get('summaries')
        return self._summaries.get('id')



    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            limit = stop - start
            page = start / limit
            query = self.shotgun.find(
                self._entity_type_type, self.filters, self.fields,
                limit=limit, page=page)
            return [ShotgunEntity(initial=data) for data in query]
        else:
            query = self.shotgun.find(
                self._entity_type_type, self.filters, self.fields)
            return ShotgunEntity(initial=query[key])

    def to_list(self):
        return self._data


class ShotgunEntityResource(Resource):
    # Just like a Django ``Form`` or ``Model``, we're defining all the
    # fields we're going to handle with the API here.
    id = fields.IntegerField(attribute='id')
    entity_type = fields.CharField(attribute='type')


    class Meta:
        #resource_name = 'entity'
        object_class = ShotgunEntity
        #authorization = Authorization()

    @property
    def _sg(self):
        if not hasattr(self, "_shotgun"):
            self._shotgun = ShotgunORM.SgConnection(
                SHOTGUN_SERVER, SHOTGUN_SCRIPT_NAME, SHOTGUN_SCRIPT_KEY)
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

    def _lazy_find(self, entity_type, filters=[], fields=[], ordering=None):


        return LazyFind(self.shotgun, entity_type, filters, fields)

    def get_object_list(self, request):
        fields_list = request.GET.get('fields', [])
        if isinstance(fields_list, str):
            fields_list = [fields_list]
        results = self.shotgun.find(self._entity_type, [], fields_list)
        return results

    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        fields_list = bundle.request.GET.get('fields', [])
        if isinstance(fields_list, str):
            fields_list = [fields_list]
        obj = self.shotgun.findOne(
            self._entity_type, [["id", "is", int(kwargs['pk'])]], fields_list)
        return ShotgunEntity(initial=obj)

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

def shotgun_entity_resource_factory(entity_type, schema=[]):
    class EntityResource(ShotgunEntityResource):
        _entity_type = entity_type

        class Meta(ShotgunEntityResource.Meta):
            resource_name = cammel_case_to_slug(entity_type)

    return EntityResource()

def shotgun_rest_api_factory(entity_types=SHOTGUN_ENTITY_TYPES):
    from tastypie.api import Api
    sg_api = Api(api_name='v3')
    for entity_type in entity_types:
        sg_api.register(shotgun_entity_resource_factory(entity_type))
    return sg_api

sg_api = shotgun_rest_api_factory()
