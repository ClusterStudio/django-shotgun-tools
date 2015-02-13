# coding: utf-8
import os

from django.conf import settings
from django.core.cache import cache

from shotgun_events import shotgunEventDaemon as sged

from shotgun_tools.utils import get_sg_connection


def patch_sged():
    class Config(sged.Config):
        def __init__(self, data):
            self.__dict__ = data

        def get(self, *args):
            value = None
            for arg in args:
                value = self.__dict__.get(arg)
            return value

        def getint(self, *args):
            value = self.get(*args)
            if value:
                return int(value)

        def has_option(self, *args):
            data = self.__dict__
            has_option = False
            for arg in args:
                has_option = arg in data.keys()
                data = data.get(arg)
                if has_option:
                    if type(data) == dict:
                        continue
                return has_option
            return value

        def getboolean(self, *args):
            return self.get(*args) == True

        def getLogFile(self, filename=None):
            return None
        def getShotgunURL(self):
            return settings.SHOTGUN_SERVER

    class DjangoPlugin(sged.Plugin):
        """
        Custom Plugins
        """
        def __init__(self, engine):
            """
            @param engine: The engine that instanciated this plugin.
            @type engine: L{Engine}
            @param path: The path of the plugin file to load.
            @type path: I{str}
            @raise ValueError: If the path to the plugin is not a valid file.
            """
            self._engine = engine

            self._pluginName = 'DjangoPlugin'
            self._active = False
            self._callbacks = []
            self._mtime = None
            self._lastEventId = None
            self._backlog = {}

            # Setup the plugin's logger
            self.logger = sged.logging.getLogger('django.' + self.getName())
            self.logger.config = self._engine.config
            #self.logger.setLevel(self._engine.config.getLogLevel())
            #if self._engine.config.getLogMode() == 1:
            #    _setFilePathOnLogger(self.logger, self._engine.config.getLogFile('plugin.' + self.getName()))

        def load(self):
            """
            Load/Reload the plugin and all its callbacks.
            If a plugin has never been loaded it will be loaded normally. If the
            plugin has been loaded before it will be reloaded only if the file has
            been modified on disk. In this event callbacks will all be cleared and
            reloaded.
            General behavior:
            - Try to load the source of the plugin.
            - Try to find a function called registerCallbacks in the file.
            - Try to run the registration function.
            At every step along the way, if any error occurs the whole plugin will
            be deactivated and the function will return.
            """
            # Check active
            if self._active:
                return
            self._engine.log.info('Loading shotgun_tools plugin')
            # Reset values
            self._callbacks = []
            self._active = True

            reg = sged.Registrar(self)
            matchEvents = {
                '*': ['*']
            }
            reg.registerCallback(
                settings.SHOTGUN_SCRIPT_NAME,
                settings.SHOTGUN_SCRIPT_KEY,
                self.django_callback,
                matchEvents)

        def django_callback(self, sg, logger, event, args):
            self._engine.log.info('Callback for: %(event_type)s attr: %(attribute_name)s' % event)

    class CustomPluginCollection(sged.PluginCollection):
        """
        Custom PluginCollection
        """
        def __init__(self, engine):

            self.path = 'shotgun_tools'

            self._engine = engine
            self._plugins = {}
            self._stateData = {}

        def load(self):
            if self._plugins:
                return
            self._plugins= {
                'shotgun_tools': DjangoPlugin(self._engine)
            }
            self._plugins['shotgun_tools'].load()

    sged.PluginCollection = CustomPluginCollection


    class CustomEngine(sged.Engine):
        """
        Customization to trigger signals
        """

        def __init__(self):
            """
            """
            self._continue = True
            self._eventIdData = {}

            # Read/parse the config
            self.config = Config({})

            # Get config values
            self._pluginCollections = [sged.PluginCollection(self)]
            self._sg = get_sg_connection()._connection
            self._max_conn_retries = self.config.getint('daemon', 'max_conn_retries') or 3
            self._conn_retry_sleep = self.config.getint('daemon', 'conn_retry_sleep') or 5
            self._fetch_interval = self.config.getint('daemon', 'fetch_interval') or 5
            self._use_session_uuid = self.config.getboolean('shotgun', 'use_session_uuid')

            # Setup the logger for the main engine
            self.log = sged.logging.getLogger('django.shotgun_events')
            self.log.config = self.config

            self.log.setLevel(self.config.getLogLevel() or 1)

        def _loadEventIdData(self):
            """
            Load the last processed event id from the disk
            If no event has ever been processed or if the eventIdFile has been
            deleted from disk, no id will be recoverable. In this case, we will try
            contacting Shotgun to get the latest event's id and we'll start
            processing from there.
            """
            events_state = cache.get("shotgun_tools_events_state")
            if events_state:
                self._eventIdData = events_state

                for collection in self._pluginCollections:
                    state = self._eventIdData.get(collection.path)
                    if state:
                        collection.setState(state)
            else:
                # No id file?
                # Get the event data from the database.
                conn_attempts = 0
                lastEventId = None
                while lastEventId is None:
                    order = [{'column':'id', 'direction':'desc'}]
                    try:
                        result = self._sg.find_one("EventLogEntry", filters=[], fields=['id'], order=order)
                    except (sg.ProtocolError, sg.ResponseError, socket.error), err:
                        conn_attempts = self._checkConnectionAttempts(conn_attempts, str(err))
                    except Exception, err:
                        msg = "Unknown error: %s" % str(err)
                        conn_attempts = self._checkConnectionAttempts(conn_attempts, msg)
                    else:
                        lastEventId = result['id']
                        self.log.info('Last event id (%d) from the Shotgun database.', lastEventId)

                        for collection in self._pluginCollections:
                            collection.setState(lastEventId)

                self._saveEventIdData()

        def _saveEventIdData(self):
            """
            Save an event Id to persistant storage.
            Next time the engine is started it will try to read the event id from
            this location to know at which event it should start processing.
            """
            for collection in self._pluginCollections:
                self._eventIdData[collection.path] = collection.getState()

            for colPath, state in self._eventIdData.items():
                if state:
                    cache.set("shotgun_tools_events_state", self._eventIdData)
                    break
            else:
                self.log.warning('No state was found. Not cacheing.')

    sged.Engine = CustomEngine

