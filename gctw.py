#!/usr/bin/env python

import gtk, weatherfeed, time

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

        menuitem = gtk.MenuItem('File')
        menuitem.set_submenu(self.file_menu())
        self.menubar1.add(menuitem)

        menuitem = gtk.MenuItem('Settings')
        menuitem.set_submenu(self.settings_menu())
        self.menubar1.add(menuitem)

        menuitem = gtk.MenuItem('Help')
        menuitem.set_submenu(self.help_menu())
        menuitem.set_right_justified(gtk.TRUE)
        self.menubar1.add(menuitem)

        button = gtk.Button("Update Weather Data")
        button.connect("clicked", self.fetch_data)
        self.vbox.pack_start(button, expand=gtk.FALSE)

        self.location = 'CAXX0343'
        self.refresh = '600'

        self.window.show_all()

    def file_menu(self):
        menu = gtk.Menu()
        menuitem = gtk.MenuItem("Exit")
        menuitem.connect('activate', self.destroy)
        menu.add(menuitem)
        return menu

    def settings_menu(self):
        menu = gtk.Menu()
        menuitem = gtk.MenuItem("Location")
        menuitem.connect('activate', self.entry_callback, "location")
        menu.add(menuitem)

        menuitem = gtk.MenuItem("Refresh Rate")
        menuitem.connect('activate', self.entry_callback, "refresh")
        menu.add(menuitem)

        return menu

    def help_menu(self):
        menu = gtk.Menu()
        menuitem = gtk.MenuItem("About CTW")
        menuitem.connect('activate', self.about_callback)
        menu.add(menuitem)
        return menu

    def error_dialog(self, message):
        dialog = gtk.MessageDialog(self.window,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                "An error occurred:\n%s" % message)
        dialog.run()
        dialog.destroy()

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

    def entry_callback(self, widget, data):
        print "Location menu item activated"
        name = data
        dialog = gtk.Dialog("Enter Location Code", self.window, 0,
                (gtk.STOCK_OK, gtk.RESPONSE_OK,
                    "Cancel", gtk.RESPONSE_CANCEL))
        hbox = gtk.HBox(gtk.FALSE, 8)
        hbox.set_border_width(8)
        dialog.vbox.pack_start(hbox, gtk.FALSE, gtk.FALSE, 0)
        stock = gtk.image_new_from_stock(
                gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(stock, gtk.FALSE, gtk.FALSE, 0)

        label = gtk.Label(name.capitalize())
        hbox.pack_start(label, gtk.FALSE, gtk.FALSE, 0)

        entry = gtk.Entry()
        entry.set_text(getattr(self, name))
        hbox.pack_start(entry, gtk.FALSE, gtk.FALSE, 0)

        dialog.show_all()

        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            setattr(self, name, entry.get_text())
            print "%s is %s" % (name, getattr(self, name))

        dialog.destroy()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return gtk.FALSE

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def show_busy(self):
        dialog = gtk.Dialog("Progress", self.window, 
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        progress = gtk.ProgressBar()
        progress.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
        progress.set_pulse_step(0.2)
        progress.set_fraction(0.5)
        progress.pulse()

        dialog.vbox.pack_start(progress, gtk.FALSE, gtk.FALSE, 0)
        dialog.connect("response", lambda dialog, response: dialog.destroy())
        dialog.show_all()
        dialog.progress = progress
        gtk.gdk.flush()

        return dialog

    def fetch_data(self, widget, data=None):
        try:
            progress = self.show_busy()
            progress.progress.pulse()
            gtk.gdk.window_process_all_updates()
            self.weather = weatherfeed.Weather(self.location)
            progress.destroy()
        except Exception, err:
            print "An error occurred: %s" % str(err)
            self.error_dialog(str(err))
            progress.destroy()

    def main(self):
        gtk.main()

if __name__ == '__main__':
    app = GCtwFrame()
    app.main()
