import eg

eg.RegisterPlugin(
    name = "Test Plugin",
    description = "Only used to demonstrate some aspects of the Plugin-API.",
)
    
import wx

class TestPlugin(eg.PluginClass):
    
    def __init__(self):
        self.AddAction(RadioButtonGridDemo)
        self.AddAction(CheckBoxGridDemo)
        self.AddAction(SpinIntCtrlDemo)
        self.AddAction(DictionaryTest)
        
        

class RadioButtonGridDemo(eg.ActionClass):
    name = "Demo eg.RadioButtonGrid"
    
    def __call__(self, *args):
        print "called with args:", repr(args)
        
    
    def Configure(self, value=()):
        dialog = eg.ConfigurationDialog(self)
        
        radioButtonGrid = eg.RadioButtonGrid(
            dialog, 
            # The columns are supplied as a sequence of strings. 
            # Each element is a column header. You can use empty strings, if
            # you wish no headers.
            columns=("1", "2", "3", "4", "5", "6", "7", "8"),
            # The same for the rows. Here we want two rows.
            rows=("Off", "On"), 
        )
        
        # SetValue() expects a sequence of integer values.
        # For RadioButtonGrids with more then one row, the values are used as 
        # indexes. For example (0, 1, 2, 1) on a RadioButtonGrid with three
        # rows will result in the following setting image:
        #     | 1 2 3 4
        #-----+--------
        # row0| X    
        # row1|   X   X
        # row2|     X
        # If the sequence is shorter than the number of columns, it will leave
        # the remaining columns untouched (they default to row0 on creation).
        radioButtonGrid.SetValue(value)
        
        dialog.sizer.Add(radioButtonGrid)
        if dialog.AffirmedShowModal():
            return (
                # GetValue() will return the index sequence of the control.
                radioButtonGrid.GetValue(),
            )
            
            
            
class CheckBoxGridDemo(eg.ActionClass):
    name = "Demo eg.CheckBoxGrid"
    
    def __call__(self, *args):
        print "called with args:", repr(args)
        
    
    def Configure(self, value=()):
        dialog = eg.ConfigurationDialog(self)
        
        checkBoxGrid = eg.CheckBoxGrid(
            dialog, 
            # The columns are supplied as a sequence of strings. 
            # Each element is a column header
            columns=("1", "2", "3", "4", "5", "6", "7", "8"),
            # The same for the rows. Here we only want one row and need
            # no header. So we give it a sequence with a single empty string
            # as value.
            rows=("",), 
        )
        
        # SetValue() expects a sequence of integer values.
        # For CheckBoxGrids with more then one row, the values are used as 
        # bitfields. For example (0, 1, 2, 3) on a CheckBoxGrid with two 
        # rows will result in the following setting image:
        #     | 1 2 3 4
        #-----+--------
        # row1|   X   X
        # row2|     X X
        # If the sequence is shorter than the number of columns, it will leave
        # the remaining columns untouched (they default to unset on creation).
        checkBoxGrid.SetValue(value)
        
        dialog.sizer.Add(checkBoxGrid)
        if dialog.AffirmedShowModal():
            return (
                # GetValue() will return the bitfield-sequence of the control.
                checkBoxGrid.GetValue(),
            )
            
    
    
class SpinIntCtrlDemo(eg.ActionClass):
    name = "Demo eg.SpinIntCtrl"
    
    def __call__(self, *args):
        print "called with:", args
        
        
    def Configure(self, value=0):
        dialog = eg.ConfigurationDialog(self)
        spinIntCtrl = eg.SpinIntCtrl(dialog, min=0, max=100, value=value)
        dialog.sizer.Add(spinIntCtrl)
        if dialog.AffirmedShowModal():
            return (spinIntCtrl.GetValue(), )
        
        
        
class DictionaryTest(eg.ActionClass):
    
    def __call__(self, a, b, c):
        print a, b, c
        
        
    def Configure(self, a=True, b="", c=""):
        panel = eg.ConfigPanel(self)
        
        aValueCtrl = panel.CheckBox(a, "Set aValue to True")
        bValueCtrl = panel.TextCtrl(b)
        cValueCtrl = panel.TextCtrl(c)
        
        panel.AddLine(aValueCtrl)
        panel.AddLine("bValue", bValueCtrl)
        panel.AddLine("cValue", cValueCtrl)
        
        while panel.Affirmed():
            panel.SetResult(
                aValueCtrl.GetValue(),
                bValueCtrl.GetValue(),
                cValueCtrl.GetValue(),
            )
        
        
        
        