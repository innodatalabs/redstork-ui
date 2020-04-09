'''Flattens PySide/PyQt namespaces, for convenience'''
from PyQt5.QtWidgets import *
#from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.Qt import *

from PyQt5.QtCore import QFile, QUrl, QIODevice, QObject
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
