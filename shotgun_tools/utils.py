# code: utf-8
import ShotgunORM
from shotgun_api3 import Shotgun

from .settings import SHOTGUN_SERVER, SHOTGUN_SCRIPT_NAME, SHOTGUN_SCRIPT_KEY

def get_sg_connection(shotgunorm=True):
    if shotgunorm:
        return ShotgunORM.SgConnection(
            SHOTGUN_SERVER, SHOTGUN_SCRIPT_NAME, SHOTGUN_SCRIPT_KEY)
    else:
        return Shotgun(SHOTGUN_SERVER, SHOTGUN_SCRIPT_NAME, SHOTGUN_SCRIPT_KEY)