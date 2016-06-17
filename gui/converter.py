#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.1 on Tue Jun 14 21:58:56 2016
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from threading import Thread
import subprocess
import os

def subprocess_thread(main, args):
    wx.CallAfter(main.status_text_ctrl.AppendText, 'Starting conversion')
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
    else:
        si = None
        env = None

    try:
        main.proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=si, env=env)
        while main.proc.poll() is None:
            line = main.proc.stdout.readline()
            if line != '':
                wx.CallAfter(main.status_text_ctrl.AppendText, line)
        main.proc.wait()
        main.proc = None
    except BaseException as exc:
        wx.CallAfter(main.status_text_ctrl.AppendText, str(exc))
    finally:
        wx.CallAfter(main.status_text_ctrl.AppendText, 'Done')
        main.convert_button.Enable()
        main.abort_button.Disable()
# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.src_dir_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.src_dir_button = wx.Button(self, wx.ID_ANY, _("Source folder"))
        self.dest_dir_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.dst_folder_button = wx.Button(self, wx.ID_ANY, _("Destination folder"))
        self.tiff_checkbox = wx.CheckBox(self, wx.ID_ANY, _("TIFF"))
        self.convert_button = wx.Button(self, wx.ID_ANY, _("Convert"))
        self.status_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.abort_button = wx.Button(self, wx.ID_ANY, _("Abort"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnSrcFolder, self.src_dir_button)
        self.Bind(wx.EVT_BUTTON, self.OnDstFolder, self.dst_folder_button)
        self.Bind(wx.EVT_BUTTON, self.OnConvert, self.convert_button)
        self.Bind(wx.EVT_BUTTON, self.OnAbort, self.abort_button)
        # end wxGlade
        self.proc = None

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle(_("SJCAM RAW Converter"))
        self.SetSize((600, 300))
        self.src_dir_button.SetFocus()
        self.tiff_checkbox.SetToolTip(wx.ToolTip(_("Convert to TIFF as well as DNG")))
        self.abort_button.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(4, 2, 0, 0)
        grid_sizer_1.Add(self.src_dir_text_ctrl, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.src_dir_button, 0, wx.ALIGN_RIGHT | wx.EXPAND, 0)
        grid_sizer_1.Add(self.dest_dir_text_ctrl, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.dst_folder_button, 0, wx.ALIGN_RIGHT | wx.EXPAND, 0)
        grid_sizer_1.Add(self.tiff_checkbox, 0, 0, 0)
        grid_sizer_1.Add(self.convert_button, 0, wx.ALL | wx.EXPAND, 2)
        grid_sizer_1.Add(self.status_text_ctrl, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.abort_button, 0, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(3)
        grid_sizer_1.AddGrowableCol(0)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnSrcFolder(self, event):  # wxGlade: MainFrame.<event_handler>
        dialog = wx.DirDialog(self, _('Choose source folder'), style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.src_dir_text_ctrl.SetValue(dialog.GetPath())
        dialog.Destroy()
        event.Skip()

    def OnDstFolder(self, event):  # wxGlade: MainFrame.<event_handler>
        dialog = wx.DirDialog(self, _('Choose destination folder'), style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.dest_dir_text_ctrl.SetValue(dialog.GetPath())
        dialog.Destroy()
        event.Skip()

    def OnConvert(self, event):  # wxGlade: MainFrame.<event_handler>
        self.status_text_ctrl.Clear()

        args = ['./sjcam_raw2dng']

        if self.tiff_checkbox.IsChecked():
            args.append('-t')

        if not self.dest_dir_text_ctrl.IsEmpty():
            args.append('-o')
            args.append(self.dest_dir_text_ctrl.GetValue())

        if self.src_dir_text_ctrl.IsEmpty():
            dlg = wx.MessageDialog(self, _('Must select source folder'), _('Error!'), wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()
            return

        args.append(self.src_dir_text_ctrl.GetValue())

        self.convert_button.Disable()
        self.abort_button.Enable()

        self.thr = Thread(target=subprocess_thread, args=(self, args))
        self.thr.daemon = True
        self.thr.start()

        event.Skip()

    def OnAbort(self, event):  # wxGlade: MainFrame.<event_handler>
        if self.proc:
            self.proc.kill()
        event.Skip()

# end of class MainFrame
if __name__ == "__main__":
    gettext.install("converter", 'locale', True) # replace with the appropriate catalog name

    converter = wx.PySimpleApp(0)
    main_frame = MainFrame(None, wx.ID_ANY, "")
    converter.SetTopWindow(main_frame)
    main_frame.Show()
    converter.MainLoop()
