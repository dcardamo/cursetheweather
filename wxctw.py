#!/usr/bin/env python
# vim: ft=python ts=2 sw=2 et:

"This is a wxPython GUI wrapper for Curse the Weather application."

from wxPython.wx import *
import weatherfeed, sys

ID_ABOUT    = 101
ID_EXIT     = 102
ID_LOCATION = 103
ID_UPDATE   = 104

about = """\
    Copyright Dan Cardamore and
Michael Soulier, 2004"""

class CtwFrame(wxFrame):
  def __init__(self, parent, ID, title):
    wxFrame.__init__(self, parent, ID, title,
        wxDefaultPosition, wxSize(500, 500))
    self.CreateStatusBar()
    self.SetStatusText("This is the statusbar")

    menuFile = wxMenu()
    menuFile.Append(ID_ABOUT, "&About",
        "More information about this program")
    menuFile.AppendSeparator()
    menuFile.Append(ID_EXIT, "E&xit", "Terminate the program")

    menuSettings = wxMenu()
    menuSettings.Append(ID_LOCATION, "&Location",
        "Set your desired location")
    menuSettings.Append(ID_UPDATE, "&Update",
        "Update weather data by current location")

    menuBar = wxMenuBar()
    menuBar.Append(menuFile, "&File");
    menuBar.Append(menuSettings, "&Settings");

    self.SetMenuBar(menuBar)

    self.location = "CAXX0343"
    self.weather = None

    EVT_MENU(self, ID_ABOUT, self.OnAbout)
    EVT_MENU(self, ID_EXIT, self.OnExit)
    EVT_MENU(self, ID_LOCATION, self.OnLocation)
    EVT_MENU(self, ID_UPDATE, self.OnUpdate)

  def OnUpdate(self, event):
    self.weather = weatherfeed.Weather(self.location)
#        max = 100
#        dialog = wxProgressDialog(
#                "Updating weather data",
#                "Please wait",
#                maximum = max,
#                parent = self,
#                style = wxPD_CAN_ABORT | wxPD_APP_MODAL)
#        keep_going = True
#        progress = 0
#        while keep_going and progress < max:
#            progress += 5
#            keep_going = dialog.Update(progress, "%d%%" % progress)
#        dialog.Destroy()

  def OnLocation(self, event):
    dialog = wxTextEntryDialog(
      self,
      "Enter location code",
      "Location",
      self.location)
    if dialog.ShowModal() == wxID_OK:
      self.location = dialog.GetValue()
      print "location is %s" % self.location
    dialog.Destroy()

  def OnAbout(self, event):
    global dialog
    dialog = wxMessageDialog(self, about, "Curse the Weather", wxOK)
    dialog.ShowModal()
    dialog.Destroy()

  def OnExit(self, event):
    self.Close(true)

class CtwGui(wxApp):
  def OnInit(self):
    frame = CtwFrame(NULL, -1, "Curse the Weather")
    frame.Show(true)
    self.SetTopWindow(frame)
    return true

def main():
  gui = CtwGui(0)
  gui.MainLoop()

if __name__ == '__main__':
  main()
