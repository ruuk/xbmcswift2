import os
from xbmcswift2.logger import log
from xbmcswift2.mockxbmc import utils


def _get_env_setting(name):
    return os.getenv('XBMCSWIFT2_%s' % name.upper())


class Addon(object):

    def __init__(self, id=None):
        # In CLI mode, xbmcswift2 must be run from the root of the addon
        # directory, so we can rely on getcwd() being correct.
        addonxml = os.path.join(os.getcwd(), 'addon.xml')
        id = id or utils.get_addon_id(addonxml)
        self._info = {
            'id': id,
            'name': utils.get_addon_name(addonxml),
            'profile': 'special://profile/addon_data/%s/' % id,
            'path': 'special://home/addons/%s' % id
        }
        self._strings = {}
        self._settings = {}

    def getAddonInfo(self, id):
        properties = ['author', 'changelog', 'description', 'disclaimer',
            'fanart', 'icon', 'id', 'name', 'path', 'profile', 'stars', 'summary',
            'type', 'version']
        assert id in properties, '%s is not a valid property.' % id
        return self._info.get(id, 'Unavailable')

    def getLocalizedString(self, id):
        key = str(id)
        assert key in self._strings, 'id not found in English/strings.po or strings.xml.'
        return self._strings[key]

    def getSetting(self, id):
        log.warning('xbmcaddon.Addon.getSetting() has not been implemented in '
                    'CLI mode.')
        try:
            value = self._settings[id]
        except KeyError:
            # see if we have an env var
            value = _get_env_setting(id)
            if _get_env_setting(id) is None:
                value = raw_input('* Please enter a temporary value for %s: ' %
                                  id)
            self._settings[id] = value
        return value

    def setSetting(self, id, value):
        self._settings[id] = value

    def openSettings(self):
        pass
