# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from .patch_sged import patch_sged
from shotgun_events import shotgunEventDaemon as sged

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'start events daemon in foreground mode'

    def handle(self, *args, **options):
        self.stdout.write('Patching shotgunEventDaemon.')
        patch_sged()
        engine = sged.Engine()
        self.stdout.write('Starting engine.')
        engine.start()

