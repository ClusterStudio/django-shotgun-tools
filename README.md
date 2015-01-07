django-shotgun-tools
====================

Bring django's magical superpowers to shotgun development.

Project Goals
-------------

* Models with ShotgunORM ... Alpha
* RestAPI: Tasypie custom resources ... Alpha
* Authentication Backend ... Alpha
* ShotgunEventDaemon Integration ... Pending

Installation
------------

´´´bash
pip install -e git+https://github.com/ClusterStudio/django-shotgun-tools#egg=django-shotgun-tools
´´´

Quick Start
-----------

´´´python
# settings.py

INSTALLED_APPS = (
    ...
    'shotgun_tools',
    ...
)

SHOTGUN_SERVER = "http://yoursite.shotgunstudio.com"
SHOTGUN_SCRIPT_NAME = "django-sgtk"
SHOTGUN_SCRIPT_KEY = "your-script-key"
´´´



