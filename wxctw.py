#!/usr/bin/env python
# vim: ft=python ts=2 sw=2 et:

"This is a wxPython GUI wrapper for Curse the Weather application."

from wxPython.wx import *
import weatherfeed, sys

ID_ABOUT    = 101
ID_EXIT     = 102
ID_LOCATION = 103
ID_UPDATE   = 104
ID_UPDATE_TIMER = 105

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
    self.SetStatusText("Fetching weather data for location %s" % self.location)
    self.count = 0
    progress = wxProgressDialog(
        "Fetching weather data for location %s" % self.location,
        "Updating",
        maximum = 100,
        parent = self,
        style = wxPD_APP_MODAL)
    self.updateTimer = CtwProgressTimer(progress)

    try:
      self.updateTimer.Start(500)
      weather = weatherfeed.Weather(self.location)
      self.SetStatusText("Weather data updated for location %s" % self.location)
      self.currentConditions = weather.currentConditions
      self.forecast = weather.forecast
    finally:
      self.updateTimer.Stop()
      self.updateTimer = None
      progress.Destroy()

  def OnProgressUpdate(self, event):
    self.count += 10
    if self.count > 100:
      self.count = 0
    self.progress.Update(self.count)

  def OnLocation(self, event):
    dialog = wxTextEntryDialog(
      self,
      "Enter location code",
      "Location",
      self.location)
    if dialog.ShowModal() == wxID_OK:
      self.location = dialog.GetValue()
      self.SetStatusText("Location set to %s" % self.location)
    dialog.Destroy()

  def OnAbout(self, event):
    dialog = wxMessageDialog(self, about, "Curse the Weather", wxOK)
    dialog.ShowModal()
    dialog.Destroy()

  def OnExit(self, event):
    self.Close(true)

class CtwProgressTimer(wxTimer):
  def __init__(self, progress):
    wxTimer.__init__(self)
    self.progress = progress
    self.count = 0

  def Notify(self):
    print "got notify event"
    self.count += 10
    self.progress.Update(self.count)
    print "timer notify called"

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
