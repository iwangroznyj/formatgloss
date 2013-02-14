#! /usr/bin/env python

'''Graphical user interface to formatgloss.

This script opens a Toolbox file and reformats glosses in it.  Opening the
input file and saving the reformatted file are accompanied by a wxPython
user interface.

'''


import wx
import formatglosslib.gui


def main():
    '''Run wx and create the main frame'''
    wxapp = wx.App()
    formatglosslib.gui.ResultsWindow(parent=None)
    wxapp.MainLoop()


if __name__ == '__main__':
    main()
