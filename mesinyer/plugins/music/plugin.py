import gobject

import extension
import songretriever

from plugin_base import PluginBase

import handler_amarok2
import handler_audacious2
import handler_banshee
import handler_gmusicbrowser
import handler_guayadeque
import handler_lastfm
import handler_moc
import handler_mpd
import handler_rhythmbox
import handler_xmms2

CATEGORY = 'listening to'

class Plugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)

        self.session = None
        self.running = False

        self.player = None

    def stop(self):
        '''stop the plugin'''
        self.session = None
        self.running = False
        return True

    def start(self, session):
        '''start the plugin'''
        self.session = session

        self.category_register()
        self.extensions_register()

        self.redraw_main_window()

        self.running = True

        return True

    def redraw_main_window(self):
        if self.session != None:
            self.session.save_config()
            self.session.signals.login_succeed.emit()
            self.session.signals.contact_list_ready.emit()

    def config(self, session):
        '''config the plugin'''
        Player = extension.get_default(CATEGORY)
        player = Player()
        if player != None:
            player.preferences()
            self.redraw_main_window()
        return True

    def category_register(self):
        ''' When you create the category with category_register, you can specify
        an interface using C{extensions.category_register("category name", IFoo)}'''
        extension.category_register(CATEGORY, songretriever.MusicHandler)
        return True

    def extensions_register(self):
        extension.register(CATEGORY, handler_amarok2.Amarok2Handler)
        extension.register(CATEGORY, handler_audacious2.Audacious2Handler)
        extension.register(CATEGORY, handler_banshee.BansheeHandler)
        extension.register(CATEGORY, handler_gmusicbrowser.GMusicBrowserHandler)
        extension.register(CATEGORY, handler_guayadeque.GuayadequeHandler)
        extension.register(CATEGORY, handler_lastfm.LastfmHandler)
        extension.register(CATEGORY, handler_moc.MocHandler)
        extension.register(CATEGORY, handler_mpd.MpdHandler)
        extension.register(CATEGORY, handler_rhythmbox.RhythmboxHandler)
        extension.register(CATEGORY, handler_xmms2.Xmms2Handler)

        #FIXME This should be configurable
        extension.set_default(CATEGORY, handler_mpd.MpdHandler)

