from wx.lib.filebrowsebutton import FileBrowseButton
from wx.lib.filebrowsebutton import DirBrowseButton
import wx
import types


def createDialog( self, parent, id, pos, size, style ):
    """Setup the graphic representation of the dialog"""
    wx.Panel.__init__ (self, parent, id, pos, size, style)
    self.SetMinSize(size) # play nice with sizers

    box = wx.BoxSizer(wx.HORIZONTAL)

    self.textControl = self.createTextControl()
    box.Add(self.textControl, 1, wx.CENTER, 5)

    self.browseButton = self.createBrowseButton()
    box.Add(self.browseButton, 0, wx.LEFT|wx.CENTER, 5)

    self.SetAutoLayout(True)
    self.SetSizer(box)
    self.Layout()
    if type(size) == types.TupleType:
        size = apply(wx.Size, size)
    self.SetDimensions(-1, -1, size.width, size.height, wx.SIZE_USE_EXISTING)


def createBrowseButton( self):
    """Create the browse-button control"""
    button = wx.BitmapButton(self, -1, wx.Bitmap("images/searchFolder.png"))
    w, h = button.GetSize()
    button.SetMinSize((w + 8, h))
    button.SetToolTipString(self.toolTip)
    button.Bind(wx.EVT_BUTTON, self.OnBrowse)
    return button


FileBrowseButton.createDialog = createDialog
FileBrowseButton.createBrowseButton = createBrowseButton

