#!/usr/bin/env python

import gtk

class GCtwFrame:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Curse the Weather")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)
        self.window.set_default_size(500, 500)

        self.vbox = gtk.VBox()
        self.window.add(self.vbox)

        self.menubar1 = gtk.MenuBar()
        self.vbox.pack_start(self.menubar1, expand=gtk.FALSE)

        menuitem = gtk.MenuItem('Settings')
        menuitem.set_submenu(self.settings_menu())
        self.menubar1.add(menuitem)

        menuitem = gtk.MenuItem('Help')
        menuitem.set_submenu(self.help_menu())
        menuitem.set_right_justified(gtk.TRUE)
        self.menubar1.add(menuitem)

        self.window.show_all()

    def settings_menu(self):
        menu = gtk.Menu()
        menuitem = gtk.MenuItem("Location")
        menuitem.connect('activate', self.location_callback)
        menu.add(menuitem)
        return menu

    def help_menu(self):
        menu = gtk.Menu()
        menuitem = gtk.MenuItem("About CTW")
        menuitem.connect('activate', self.about_callback)
        menu.add(menuitem)
        return menu

    def about_callback(self, widget, data=None):
        print "About menu item activated"
        dialog = gtk.MessageDialog(
                self.window,
                gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO,
                gtk.BUTTONS_OK,
                "Curse the Weather\nCopyright (c) Dan Cardamore\n"
                "and Michael P. Soulier")
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()

    def location_callback(self, widget, data=None):
        print "Location menu item activated"

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return gtk.FALSE

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

    def create_menu(self):
        self.menubar = gtk.MenuBar()
        self.menu = gtk.Menu()


if __name__ == '__main__':
    app = GCtwFrame()
    app.main()
