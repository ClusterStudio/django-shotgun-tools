# code: utf-8
import ShotgunORM

from .settings import SHOTGUN_SERVER, SHOTGUN_SCRIPT_NAME, SHOTGUN_SCRIPT_KEY

def get_sg_connection():
    return ShotgunORM.SgConnection(
        SHOTGUN_SERVER, SHOTGUN_SCRIPT_NAME, SHOTGUN_SCRIPT_KEY)