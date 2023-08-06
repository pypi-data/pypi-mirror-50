"""
    frames/basic_panels.py: Defines basic controls commonly used in applications

    This file is part of the PyXperiment project.

    Copyright (c) 2019 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import wx

class TextPanel(wx.Panel):
    def __init__(self,parent,ID=wx.ID_ANY,initval='',size=(35,-1),style=0,show_mod=False):
        wx.Panel.__init__(self,parent,ID)
        self.lastSetValue = initval
        self.edit = wx.TextCtrl(
            self, -1, 
            size=size,
            value=initval,
            style=style
            )
        if show_mod:
            self.Bind(wx.EVT_TEXT, self.OnTextChange, self.edit)
    
    def OnTextChange(self,event):
        if self.IsModified():
            self.edit.SetForegroundColour((255, 0, 0))
        else:
            self.edit.SetForegroundColour((0, 0, 0))
        wx.PostEvent(self.Parent.GetEventHandler(), event)

    def SetEnabled(self, value):
        if value:
            self.edit.Enable()
        else:
            self.edit.Disable()

    def SetEditable(self, value):
        self.edit.SetEditable(value)
                
    def GetValue(self):
        return self.edit.Value

    def SetValue(self, value):
        self.lastSetValue = value
        self.edit.Value = value

    def IsModified(self):
        return self.edit.Value != self.lastSetValue

class BoxedTextPanel(TextPanel):
    def __init__(self,parent,label,ID=wx.ID_ANY,initval='',size=(35,-1),style=0,show_mod=False):
        TextPanel.__init__(self,parent,ID,initval,size,style,show_mod)
        box = wx.StaticBox(self, -1, label)
        self.sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.sizer.Add(self.edit, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

class CaptionTextPanel(TextPanel):
    def __init__(self,parent,label,ID=wx.ID_ANY,initval='',size=(35,-1),style=0,orienation=wx.HORIZONTAL,show_mod=False):
        TextPanel.__init__(self,parent,ID,initval,size,style,show_mod)
        box = wx.StaticBox(self, -1, label)
        self.sizer = wx.StaticBoxSizer(box, orienation)
        self.sizer.Add(self.edit, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        
class CaptionDropBox(wx.Panel):
    def __init__(self,parent,label,values=[],ID=wx.ID_ANY,orienation=wx.HORIZONTAL):
        wx.Panel.__init__(self,parent,ID)
        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, orienation)
        
        self.__combo = wx.ComboBox(self, style = wx.CB_READONLY)
        for value in values:
            self.__combo.Append(value)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_change, self.__combo)
        self.__modified = False

        sizer.Add(self.__combo, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def SetItems(self,items):
        self.__combo.Clear()
        for item in items:
            self.__combo.Append(item)
    
    def SetEnabled(self,value):
        if value:
            self.__combo.Enable()
        else:
            self.__combo.Disable()

    def SetEditable(self,value):
        self.__combo.SetEditable(value)

    def on_combo_change(self, event):
        self.__combo.SetForegroundColour((255,0,0))
        self.__modified = True

    def SetValue(self,value):
        self.__combo.SetSelection(self.__combo.Items.index(value))
        self.__combo.SetForegroundColour((0,0,0))
        self.__modified = False
        
    def GetValue(self):
        value = self.__combo.GetSelection()
        return self.__combo.Items[value]
    
    def IsModified(self):
        return self.__modified

class ModifiedCheckBox(wx.CheckBox):
    
    def __init__(self,parent,label,ID=wx.ID_ANY):
        wx.CheckBox.__init__(self,parent,ID,label=label,style=wx.CHK_3STATE)
        self.Set3StateValue(wx.CHK_UNDETERMINED)
        self.Bind(wx.EVT_CHECKBOX, self.__on_check_change, self)
        self.__modified = False
        
    def __on_check_change(self, event):
        self.SetForegroundColour((255,0,0))
        self.__modified = True

    def SetValue(self,value):
        self.Set3StateValue(wx.CHK_CHECKED if value else wx.CHK_UNCHECKED)
        self.SetForegroundColour((0,0,0))
        self.__modified = False
        
    def GetValue(self):
        return self.Get3StateValue() == wx.CHK_CHECKED

    def IsModified(self):
        return self.__modified

    def SetEnabled(self,value):
        if value:
            self.Enable()
        else:
            self.Disable()

    