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
    # Make the top level frame
    wxFrame.__init__(self, parent, ID, title,
        wxDefaultPosition, wxSize(500, 500))

    # A bold font for later use.
    self.bfont = wxFont(
        self.GetFont().GetPointSize(),
        self.GetFont().GetFamily(),
        self.GetFont().GetStyle(),
        wxBOLD)

    self.CreateStatusBar()
    self.SetStatusText("This is the statusbar")

    self.make_menu()

    left_panel = self.make_left_panel()
    right_panel = self.make_right_panel()

    box_sizer = wxBoxSizer(wxHORIZONTAL)
    box_sizer.Add(left_panel, 1, wxEXPAND)
    box_sizer.Add(right_panel, 2, wxEXPAND)

    self.SetAutoLayout(true)
    self.SetSizer(box_sizer)
    self.Layout()

    self.location = "CAXX0343"
    self.weather = None

  def make_left_panel(self):
    left_panel = wxPanel(self, -1, size=(50,50), style=wxNO_BORDER)
    left_panel.SetBackgroundColour("WHITE")

    left_panelbox = wxStaticBox(left_panel,
                                -1,
                                "Current Conditions",
                                size=(50,50))
    left_panelbox.SetFont(self.bfont)

    left_panelbox_sizer = wxStaticBoxSizer(left_panelbox, wxVERTICAL)

    left_panel.SetAutoLayout(true)
    left_panel.SetSizer(left_panelbox_sizer)
    left_panel.Layout()
    return left_panel

  def make_right_panel(self):
    right_panel = wxPanel(self, -1, size=(50,50), style=wxNO_BORDER)
    right_panel.SetBackgroundColour("WHITE")

    right_panelbox = wxStaticBox(right_panel,
                                 -1,
                                 "Forecast Conditions",
                                 size=(50,50))
    right_panelbox.SetFont(self.bfont)

    right_panelbox_sizer = wxStaticBoxSizer(right_panelbox, wxVERTICAL)

    grid_sizer = self.make_forecast_grid(right_panel)

    right_panelbox_sizer.Add(grid_sizer,
                             1,
                             wxALL | wxEXPAND | wxALIGN_CENTER,
                             4)

    right_panel.SetAutoLayout(true)
    right_panel.SetSizer(right_panelbox_sizer)
    right_panel.Layout()
    return right_panel

  def make_forecast_grid(self, parent_panel):
    grid_sizer = wxGridSizer(5, 2, 1, 1)

    i = 0
    for j in range(10):
      i += 1
      label = "Label %d" % i
      staticbox = wxStaticBox(parent_panel,
                              -1,
                              label,
                              size=(50,50))
      sbsizer = wxStaticBoxSizer(staticbox, wxVERTICAL)
      grid_sizer.Add(staticbox, 1, wxEXPAND)

    return grid_sizer

  def make_menu(self):
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
