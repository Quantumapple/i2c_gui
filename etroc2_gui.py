import tkinter as tk
import tkinter.ttk as ttk
import logging

import i2c_gui

def main():
    root = tk.Tk()
    i2c_gui.__no_connect__ = True
    i2c_gui.set_swap_endian()
    i2c_gui.set_platform(root.tk.call('tk', 'windowingsystem'))

    # Only for development purposes, uncomment to have a preview of the window in windows while running on macOS
    style = ttk.Style(root)
    #style.theme_use('classic')

    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s:%(name)s:%(message)s')
    logger = logging.getLogger("GUI_Logger")

    GUI = i2c_gui.ETROC2_GUI(root, logger)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    root.mainloop()

if __name__ == "__main__":
    main()