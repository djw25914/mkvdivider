try:
    from PyKDE4.kdecore import *
    from PyKDE4.kdeui import *
    from PyKDE4.kio import KDirSelectDialog
    from PyKDE4 import kdecore, kdeui
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import QtCore, QtGui
except:
    print("MyDirRequester is a PyKDE4 widget - it requires PyQt4 and PyKDE4 to be installed to work.")
    sys.exit(2)
    
from PyQt4 import QtCore

qt_resource_data = b"\
\x00\x00\x02\x8c\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\
\x00\x00\x00\x01\x73\x52\x47\x42\x00\xae\xce\x1c\xe9\x00\x00\x00\
\x06\x62\x4b\x47\x44\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\
\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0d\xd7\x00\x00\x0d\xd7\x01\
\x42\x28\x9b\x78\x00\x00\x00\x07\x74\x49\x4d\x45\x07\xdb\x05\x08\
\x11\x2b\x36\x1d\x57\x40\x64\x00\x00\x02\x0c\x49\x44\x41\x54\x38\
\xcb\x8d\x92\xcf\x4b\x55\x51\x10\xc7\x3f\x33\xf7\x78\x9f\xba\x2c\
\xa8\xa0\x45\xb9\x2c\x23\xa1\x1f\xae\x32\x17\xa6\x21\x41\x10\xb8\
\x69\xd7\xbe\x5d\xad\x82\xc0\xff\x26\xa2\x88\x36\x49\x51\x54\x10\
\x22\x46\x06\x42\x16\xb5\x28\x88\x8c\x44\x2d\x7a\xbe\x7c\xe6\xbd\
\xf7\xcc\xb4\xb8\xf7\xbd\xae\x50\xd4\x6c\x0e\x67\x98\xf9\xfe\x62\
\xe0\x2f\x35\x35\x7d\x8f\xff\x29\x99\x9a\x9e\x79\x1e\x45\x87\x71\
\x10\x00\x17\x42\x9a\xbc\xbe\x75\x7d\xfc\xc8\xbf\x96\xa7\xa6\x67\
\x90\xc9\x2b\x37\x7c\xe2\xec\x24\x1e\x73\x54\x85\x24\x09\x3c\x78\
\xf2\xcc\xd3\x34\x15\x24\x41\x01\x03\x54\x01\x07\x91\x0e\x49\xe3\
\xcd\xcd\x6b\xa7\x07\xc3\x8f\xe6\x3a\x5b\xed\x0d\x16\xdf\xaf\xa3\
\x28\x03\x7b\xfb\x18\x1d\x1e\x12\x43\x70\xc0\xdc\x70\x57\x62\x8c\
\x98\x0b\x66\x06\xda\xc3\xc2\xcb\x17\x87\x01\xc2\xc6\xb7\x15\x9a\
\xad\x4d\x8a\xad\x4d\x12\x85\x77\x1f\x5b\xc4\x3c\xb2\xb6\xb6\xcc\
\x66\xf3\x3b\xd6\xb1\x26\xa5\x82\xe8\x30\xb0\x7f\x37\x8b\x73\x8f\
\xcb\x0c\x0e\x8e\x5c\xf2\x43\xc7\x47\xf9\xf0\x69\x8d\x44\x05\x10\
\x7e\x6e\xb5\x38\x37\x76\x8c\x0b\xe7\xc7\x30\xf3\x7a\x64\x80\xd1\
\x08\x09\x96\xa4\xbc\x5d\x7a\xf5\x28\x9c\x38\x35\xca\xd5\xcb\x17\
\x69\xb5\xb7\x51\x15\x00\xdc\x85\xed\xed\x8c\xc5\xa5\x15\xb2\xdc\
\x90\x6a\x95\x52\x04\x21\x08\x12\x7a\x79\x7a\xe7\xf6\x78\xf0\xa4\
\x9f\xd9\x85\x2f\x14\x59\xd6\x1d\x00\x50\x11\x3c\x81\x1e\x2d\x43\
\xf4\x0a\x44\x80\x68\x4e\x43\x14\xd1\x40\x70\x17\x54\x80\x8a\x3d\
\x01\x62\x07\xc8\x20\x03\x42\xd5\x93\x9a\x99\xc2\x1c\x1c\x82\x7b\
\xf9\x89\xe6\x08\x50\x00\x4a\x19\x96\x48\xb9\x94\x55\x80\xda\x01\
\x76\x30\x73\x0a\x77\x82\xbb\x63\xd1\x29\xa2\xef\xf0\xe9\xdd\xc8\
\x7e\x97\xd7\x2c\x16\xd1\x70\x73\x82\x88\xa0\x9a\x90\xa8\x75\x2d\
\x74\xd8\xac\x7a\xa5\x06\x56\xf6\x1d\x4d\x12\x14\x21\xac\x7c\x6d\
\x72\x7f\x7e\x09\xb7\x62\x07\x93\xd6\x54\xf8\x1f\xce\x38\xa4\x7d\
\x2c\x7f\x5e\x25\x1c\xd8\xb7\x8b\xa1\xa3\x83\xc4\x22\xef\x32\xd5\
\xa5\xd6\x7b\x56\x03\x4e\x1b\x7d\xcc\xad\xce\x13\x36\xda\xd9\xc3\
\x2c\xb7\x89\x22\x77\x44\xc0\xbc\x0c\xb2\x87\xea\xee\x2b\x49\x79\
\x05\x14\x04\x70\x27\x12\x69\xe7\x7e\x57\xd8\x73\xf2\x0c\x45\x3e\
\x02\x08\xee\x8a\x20\xb8\x4b\xd7\xbe\x3b\x88\x54\x02\xa4\x14\x27\
\x62\x38\x4e\x6f\xff\xec\x2f\xfc\x57\xfc\x49\x4c\xef\x79\xa6\x00\
\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x06\
\x07\x03\x7d\xc3\
\x00\x69\
\x00\x6d\x00\x61\x00\x67\x00\x65\x00\x73\
\x00\x0a\
\x0a\xc8\xfb\x07\
\x00\x66\
\x00\x6f\x00\x6c\x00\x64\x00\x65\x00\x72\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x12\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()


class MyDirRequester(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setObjectName("MyDirRequester")
        
        self.widget = QWidget()
        self.layout = QHBoxLayout(self.widget)
        
        self.editor = KLineEdit(self.widget)
        self.editor.setReadOnly(True)
        self.editor.setObjectName("Editor")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/folder.png"))
        
        self.openFolder = QtGui.QToolButton()
        self.openFolder.setIcon(icon)
        self.openFolder.setObjectName("openFolder")
        
        self.selecterDialog = KDirSelectDialog()
        
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.openFolder)
        
        self.setLayout(self.layout)
        
        self.openFolder.clicked.connect(self.launchOpener)
        self.editor.textChanged.connect(self.reportChange)
        QtCore.QObject.connect(self, QtCore.SIGNAL("directoryChanged()"),self.doNothing)

    def retranslateUi(self, MyDirRequester):
        MyDirRequester.setWindowTitle(kdecore.i18n("Form"))

    def launchOpener(self):
        unstringed = self.selecterDialog.selectDirectory(KUrl(self.editor.text()))
        stringed = (unstringed.url())
        self.editor.setText(stringed)
        
    def reportChange(self):
        self.emit(QtCore.SIGNAL("directoryChanged()"))
        
    def clear(self):
        self.editor.clear()
        
    def url(self):
        return KUrl(self.editor.text()).path()
        
    def setText(self, text):
        self.editor.setText(text)
        
    def doNothing(self):
        pass
