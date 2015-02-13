# coding: utf-8
import ShotgunORM

ShotgunORM.SgSchema.registerDefaultQueryFields(
  sgEntityType='Project',
  sgQueryTemplates=['default'],
  sgFields=[
    'name',
    'sg_status',
    'sg_code',
  ]
)

ShotgunORM.SgSchema.registerDefaultQueryFields(
  sgEntityType='Version',
  sgQueryTemplates=['default'],
  sgFields=[
    'code',
    'project',
    'sg_first_frame',
    'sg_path_to_frames',
    'sg_last_frame',
    'sg_uploaded_movie',
    'image',
    'created_by',
  ]
)