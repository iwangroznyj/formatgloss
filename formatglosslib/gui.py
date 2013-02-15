'''Graphical user interface to Formatgloss.

This module contains the wxPython user interface to formatgloss.
This script opens a Toolbox file and reformats glosses in it.  Opening the
input file and saving the reformatted file are accompanied by a wxPython
user interface.

'''


import os.path
import wx
import formatglosslib.tbgloss as tbgloss


# window strings
MSG_TITLE = 'Toolbox gloss formatter'

# status messages
MSG_NOFILE = 'No text file opened.'
MSG_FILEEMPTY = 'File "{0}" is empty.'
MSG_SUCCESS = 'Opened file "{0}".'
MSG_REPORT = '''Report
 * {number} glosses detected
 * {faulty} glosses cannot be formatted'''

# dialogs
MSG_OPEN = 'Open Toolbox text file'
MSG_SAVE = 'Save formatted Toolbox text file'
MSG_ERROR = 'Error'
MSG_INFO = 'Information'


class OpenDialog(wx.FileDialog):
    ''''Open file' dialog'''
    def __init__(self, parent):
        '''Initialise 'open file' dialog.

        :param parent: parent window of the dialog
        :type  parent: wx.Window

        '''
        super(OpenDialog, self).__init__(parent,
                                         message=MSG_OPEN,
                                         style=wx.FD_OPEN)


class SaveDialog(wx.FileDialog):
    ''''Save file' dialog'''
    def __init__(self, parent):
        '''Initialise 'open file' dialog.

        :param parent: parent window of the dialog
        :type  parent: wx.Window

        '''
        super(SaveDialog, self).__init__(parent,
                                         message=MSG_SAVE,
                                         style=wx.FD_SAVE |
                                         wx.FD_OVERWRITE_PROMPT)


class ErrorDialog(wx.MessageDialog):
    '''Dialog for showing error messages'''
    def __init__(self, parent, message):
        '''Create, show and destroy error message.

        :param parent:  parent window of the dialog
        :type  parent:  wx.Window
        :param message: error message
        :type  message: str

        '''
        super(ErrorDialog, self).__init__(parent=parent,
                                          message=message,
                                          caption=MSG_ERROR,
                                          style=wx.OK | wx.ICON_ERROR)
        self.ShowModal()
        self.Destroy()


class MessageDialog(wx.MessageDialog):
    '''Dialog for showing messages'''
    def __init__(self, parent, message):
        '''Create, show and destroy message.

        :param parent:  parent window of the dialog
        :type  parent:  wx.Window
        :param message: error message
        :type  message: str

        '''
        super(MessageDialog, self).__init__(parent=parent,
                                            message=message,
                                            caption=MSG_INFO,
                                            style=wx.OK | wx.ICON_INFORMATION)
        self.ShowModal()
        self.Destroy()


class ShowGlossesDialog(wx.Dialog):
    '''Dialog for showing faulty glosses'''
    def __init__(self, parent, toolbox_file):
        '''Initialise dialog.

        :param parent:       parent window of the dialog
        :type  parent:       wx.Window
        :param toolbox_file: toolbox file to be displayed
        :type  toolbox_file: tbgloss.ToolboxFile

        '''
        super(ShowGlossesDialog, self).__init__(parent)
        self.toolbox_file = toolbox_file
        self.init_ui()
        self.ShowModal()
        self.Destroy()

    def init_ui(self):
        '''Initialise widgets'''
        # window properties
        self.SetTitle('Faulty glosses')
        self.SetSize((350, 250))
        lbl = wx.StaticText(parent=self,
                            label='Following glosses cannot be formatted:')
        textctrl = wx.TextCtrl(parent=self, style=wx.TE_MULTILINE)
        textctrl.SetEditable(False)
        textctrl.SetValue(self._format_glosses().decode('utf-8'))
        # layout
        vsizer = wx.BoxSizer(orient=wx.VERTICAL)
        vsizer.Add(lbl, flag=wx.ALL, border=3)
        vsizer.Add(textctrl, proportion=1, flag=wx.ALL | wx.EXPAND, border=3)
        bsizer = self.CreateStdDialogButtonSizer(wx.OK)
        vsizer.Add(bsizer, flag=wx.ALL, border=3)
        self.SetSizer(vsizer)

    def _format_glosses(self):
        '''Filter and format faulty glosses'''
        glosses = ['Gloss:\n{0}\nError: {1}\n'.format(gloss, gloss.error)
                   for gloss in self.toolbox_file.get_glosses()
                   if gloss.is_faulty]
        return '\n'.join(glosses)


class GlossReport(wx.StaticText):
    '''Static text which reports occurring faulty Toolbox glosses'''

    def __init__(self, parent, label):
        '''Initialise gloss report.

        :param parent: parent window of the gloss report
        :type  parent: wx.Window
        :param label:  initial label text
        :type  label:  str

        '''
        super(GlossReport, self).__init__(parent, label=label)
        self.toolbox_file = tbgloss.ToolboxFile()

    def _update(self):
        '''Update text of the report'''
        if not self.toolbox_file:
            filename = self.GetParent().filename
            self.SetLabel(MSG_FILEEMPTY.format(os.path.basename(filename)))
            return
        gloss_list = self.toolbox_file.get_glosses()
        faulty_list = [gloss for gloss in gloss_list if gloss.is_faulty]
        self.SetLabel(MSG_REPORT.format(number=len(gloss_list),
                                        faulty=len(faulty_list)))

    def set_toolbox_file(self, toolbox_file):
        '''Set a new toolbox file and update report

        :param toolbox_file: new Toolbox file
        :type  toolbox_file: tbgloss.ToolboxFile

        '''
        self.toolbox_file = toolbox_file
        self._update()


class ResultsWindow(wx.Frame):
    '''Main frame of the application'''

    def __init__(self, parent):
        '''Initialise main frame.

        :param parent: parent window of the frame
        :type  parent: wx.Window

        '''
        super(ResultsWindow, self).__init__(parent)
        self.toolbox_file = tbgloss.ToolboxFile()
        self.filename = ''
        self.init_ui()
        self.reset_window()
        self.Show()

    def init_ui(self):
        '''Initialise user interface of the frame'''
        # window settings
        self.SetTitle(MSG_TITLE)
        self.SetSize((300, 170))

        # menu
        menubar = wx.MenuBar()
        menufile = wx.Menu()
        menufile.Append(id=wx.ID_OPEN, text='&Open...\tCtrl-O')
        self.filesave = menufile.Append(id=wx.ID_SAVE, text='&Save...\tCtrl-S')
        menufile.AppendSeparator()
        self.fileclose = menufile.Append(id=wx.ID_CLOSE,
                                         text='&Close file\tCtrl-W')
        menufile.Append(id=wx.ID_EXIT, text='&Quit\tCtrl-Q')
        menubar.Append(menufile, '&File')
        menutools = wx.Menu()
        self.toolsshow = menutools.Append(id=wx.ID_ANY, text='Show &errors')
        menubar.Append(menutools, '&Tools')
        self.SetMenuBar(menubar)

        # widgets
        # workaround for the 'ugly dark-grey background problem' in Windows
        panel = wx.Panel(parent=self)
        self.label = wx.StaticText(parent=panel, label=MSG_NOFILE)
        line = wx.StaticLine(parent=panel)
        self.report = GlossReport(parent=panel, label='')
        openbutton = wx.Button(parent=panel, id=wx.ID_OPEN, label='&Open')
        self.showbutton = wx.Button(parent=panel, label='Show &Errors')
        self.savebutton = wx.Button(parent=panel, id=wx.ID_SAVE, label='&Save')

        # layout
        vsizer = wx.BoxSizer(orient=wx.VERTICAL)
        vsizer.Add(self.label, flag=wx.ALL, border=5)
        vsizer.Add(line, flag=wx.EXPAND | wx.ALL, border=5)
        vsizer.Add(self.report,
                   proportion=1,
                   flag=wx.EXPAND | wx.ALL,
                   border=5)
        gsizer = wx.GridSizer(rows=1, cols=3)
        gsizer.Add(openbutton, flag=wx.ALL, border=5)
        gsizer.Add(self.showbutton, flag=wx.ALL, border=5)
        gsizer.Add(self.savebutton, flag=wx.ALL, border=5)
        vsizer.Add(gsizer)
        panel.SetSizer(vsizer)

        # events
        self.Bind(event=wx.EVT_BUTTON, handler=self.on_open, id=wx.ID_OPEN)
        self.Bind(event=wx.EVT_BUTTON, handler=self.on_show,
                  source=self.showbutton)
        self.Bind(event=wx.EVT_BUTTON, handler=self.on_save, id=wx.ID_SAVE)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open, id=wx.ID_OPEN)
        self.Bind(event=wx.EVT_MENU, handler=self.on_save, id=wx.ID_SAVE)
        self.Bind(event=wx.EVT_MENU, handler=self.on_close, id=wx.ID_CLOSE)
        self.Bind(event=wx.EVT_MENU, handler=self.on_quit, id=wx.ID_EXIT)
        self.Bind(event=wx.EVT_MENU, handler=self.on_show,
                  source=self.toolsshow)

    def disable_save(self):
        '''Disable 'save' widgets'''
        self.filesave.Enable(False)
        self.fileclose.Enable(False)
        self.savebutton.Enable(False)

    def disable_show(self):
        '''Disable 'show' widgets'''
        self.toolsshow.Enable(False)
        self.showbutton.Enable(False)

    def enable_save(self):
        '''Enable disabled 'save' widgets'''
        self.filesave.Enable()
        self.fileclose.Enable()
        self.savebutton.Enable()
        self.savebutton.SetDefault()
        self.savebutton.SetFocus()

    def enable_show(self):
        '''Enable disabled 'show' widgets'''
        self.toolsshow.Enable()
        self.showbutton.Enable()

    def on_open(self, event):
        '''Handle 'open' event'''
        self.read_toolbox_file()

    def on_show(self, event):
        '''Handle 'show glosses' event'''
        ShowGlossesDialog(parent=self, toolbox_file=self.toolbox_file)

    def on_close(self, event):
        '''Handle 'close' event'''
        self.reset_window()

    def on_quit(self, event):
        '''Handle 'exit' event'''
        self.Close()

    def on_save(self, event):
        '''Handle 'save' event'''
        dlg = SaveDialog(parent=self)
        answer = dlg.ShowModal()
        filename = dlg.GetPath()
        dlg.Destroy()
        if not answer == wx.ID_OK:
            returnn
        try:
            with open(filename, 'w') as outputfile:
                outputfile.write(str(self.toolbox_file))
        except IOError as error:
            ErrorDialog(parent=None, message=str(error))
        else:
            MessageDialog(parent=self, message='File was saved successfully.')

    def read_toolbox_file(self):
        '''Read Toolbox glosses from file'''
        dlg = OpenDialog(parent=self)
        answer = dlg.ShowModal()
        filename = dlg.GetPath()
        dlg.Destroy()
        if not answer == wx.ID_OK:
            return
        try:
            with open(filename, 'r') as inputfile:
                content = inputfile.readlines()
            content = [unicode(line.strip(), tbgloss.INPUT_ENC)
                       for line in content]
        except IOError as error:
            ErrorDialog(parent=self, message=str(error))
        else:
            self.toolbox_file = tbgloss.ToolboxFile(content)
            self.report.set_toolbox_file(self.toolbox_file)
            self.filename = filename
            self.label.SetLabel(MSG_SUCCESS.format(os.path.basename(filename)))
            self.enable_save()
            if any(gloss.is_faulty
                   for gloss in self.toolbox_file.get_glosses()):
                self.enable_show()
            else:
                self.disable_show()

    def reset_window(self):
        '''Reset window to defaults'''
        self.filename = ''
        self.disable_save()
        self.disable_show()
        self.label.SetLabel(MSG_NOFILE)
        self.report.SetLabel('')
