# code: utf-8
from tastypie import fields
from shotgun_tools.api import shotgun_entity_resource_factory

ProjectResource = shotgun_entity_resource_factory("Project")
NoteResource = shotgun_entity_resource_factory("Note")

VersionResourceBase = shotgun_entity_resource_factory("Version")

class VersionResource(VersionResourceBase):
    project = fields.ToOneField(ProjectResource, 'project', full=False, null=True)
    notes = fields.ToManyField(NoteResource, 'notes', full=False, null=True)
