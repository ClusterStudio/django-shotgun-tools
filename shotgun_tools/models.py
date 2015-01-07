from django.db import models

import ShotgunORM

from .settings import SHOTGUN_ENTITY_TYPES, SHOTGUN_AUTO_REGISTER_SG_ENTITY_BASE_CLASS


class SgEntityBase(ShotgunORM.SgEntity):
	'''
	SgEntityBase class for easier tastypie integration.
	'''

	@property
	def pk(self):
	    return self.id

	def __getattribute__(self, item):
		value = super(SgEntityBase, self).__getattribute__(item)

		# This is a workaround for a bug in the api.
		if isinstance(value, basestring):
			return value.decode('utf-8')

		# For compatibility with tastypie.fields.ToManyField
		if isinstance(value, list):
			class list_wrapper(list):
				def all(self):
					return self
			value = list_wrapper(value)

		return value


if SHOTGUN_AUTO_REGISTER_SG_ENTITY_BASE_CLASS:
	ShotgunORM.SgEntity.registerDefaultEntityClass(
	  sgEntityCls=SgEntityBase,
	  sgEntityTypes=SHOTGUN_ENTITY_TYPES
	)