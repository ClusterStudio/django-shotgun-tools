# coding: utf-8
from django.conf import settings

SHOTGUN_SERVER = getattr(settings, "SHOTGUN_SERVER")
SHOTGUN_SCRIPT_NAME = getattr(settings, "SHOTGUN_SCRIPT_NAME", "django-sgtk")
SHOTGUN_SCRIPT_KEY = getattr(settings, "SHOTGUN_SCRIPT_KEY")
SHOTGUN_API_NAME = getattr(settings, "SHOTGUN_API_NAME", "")

###############################################################################################
# Constants
SHOTGUN_ENTITY_TYPES = ['Playlist', 'AssetSceneConnection', 'Note', 'TaskDependency', 'PageHit',
                        'ActionMenuItem', 'Attachment', 'AssetMocapTakeConnection',
                        'Department', 'Group', 'PlaylistVersionConnection',
                        'Booking', 'CutVersionConnection', 'CameraMocapTakeConnection',
                        'AssetElementConnection', 'ReleaseTicketConnection',
                        'RevisionRevisionConnection', 'MocapTakeRangeShotConnection', 'TimeLog',
                        'Step', 'AssetBlendshapeConnection', 'PerformerMocapTakeConnection',
                        'Phase', 'Ticket', 'AssetShotConnection', 'TicketTicketConnection',
                        'Icon', 'PageSetting', 'Status', 'Reply', 'Task', 'ApiUser',
                        'ProjectUserConnection', 'LaunchShotConnection', 'ShotShotConnection',
                        'PerformerRoutineConnection', 'AppWelcomeUserConnection', 'HumanUser',
                        'Project', 'LocalStorage', 'TaskTemplate', 'RevisionTicketConnection',
                        'PerformerShootDayConnection', 'PipelineConfiguration', 'LaunchSceneConnection',
                        'GroupUserConnection', 'AssetSequenceConnection', 'Page',
                        'ShootDaySceneConnection', 'TankType', 'PhysicalAssetMocapTakeConnection',
                        'Shot', 'TankPublishedFile', 'Sequence', 'BannerUserConnection',
                        'AssetAssetConnection', 'Version', 'ElementShotConnection',
                        'PermissionRuleSet', 'EventLogEntry', 'TankDependency',
                        'PublishedFile', 'PublishedFileType', 'PublishedFileDependency',
                        'AssetShootDayConnection', 'Asset']

SHOTGUN_ENTITY_TYPES.extend(["CustomEntity%02d"%x for x in range(1, 31)])
SHOTGUN_ENTITY_TYPES.extend(["CustomNonProjectEntity%02d"%x for x in range(1, 16)])
SHOTGUN_ENTITY_TYPES.extend(["CustomThreadedEntity%02d"%x for x in range(1, 6)])

SHOTGUN_AUTO_REGISTER_SG_ENTITY_BASE_CLASS = getattr(settings, "SHOTGUN_AUTO_REGISTER_SG_ENTITY_BASE_CLASS", True)