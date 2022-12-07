from __future__ import annotations

from .gui_helper import GUI_Helper
from .base_gui import Base_GUI

import tkinter as tk
import tkinter.font
import tkinter.ttk as ttk  # For themed widgets (gives a more native visual to the elements)
import logging

class About_Helper(GUI_Helper):
    _parent: Base_GUI
    def __init__(self, parent: Base_GUI):
        super().__init__(parent, None, parent._logger)

    def display_about(self):
        if hasattr(self, "_about_window"):
            self._logger.info("About window already open")
            return

        self._about_window = tk.Toplevel(self._parent._root)
        self._about_window.protocol('WM_DELETE_WINDOW', self.close_about_window)

        self._about_window.title("About " + self._parent._title)
        self._about_window.geometry("500x500")
        self._about_window.resizable(0, 0)
        self._about_window.columnconfigure(100, weight=1)
        self._about_window.rowconfigure(100, weight=1)

        self._frame = ttk.Frame(self._about_window, padding="5 5 5 5")
        self._frame.grid(column=100, row=100, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._frame.columnconfigure(100, weight=1)

        self._about_title = tk.Label(self._frame, text=self._parent._title, font=('arial', 20, tkinter.font.BOLD))
        self._about_title.grid(column=100, row=100, sticky='')

        self._parent._about_contents(self._frame, column=100, row=200)

        from . import __version__
        self._about_info_label = tk.Label(self._frame, text="I2C GUI Library - v{}".format(__version__))
        self._about_info_label.grid(column=100, row=2000, sticky='', pady=(20,0))

        self._about_copy_label = tk.Label(self._frame, justify=tk.LEFT, wraplength=490, text="Tool written and developed by Cristóvão Beirão da Cruz e Silva - © 2022")
        self._about_copy_label.grid(column=100, row=2100, sticky=tk.S)

    def close_about_window(self):
        if not hasattr(self, "_about_window"):
            self._logger.info("About window does not exist")
            return

        self._about_window.destroy()
        del self._about_window
