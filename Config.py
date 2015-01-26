
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtOpenGL import *


class SimControl(QWidget):
    def __init__(self):
        super(SimControl, self).__init__()
        
        box = QVBoxLayout()
        
        hello = QPushButton('Hello')
        hello.clicked.connect(self.hello)
        error = QPushButton('Error')
        error.clicked.connect(self.error)
        quit = QPushButton('Quit')
        quit.clicked.connect(self.quit)
        
        box.addWidget(hello)
        box.addWidget(error)
        box.addWidget(quit)
        
        box.setProperty('spacing', 0)
        box.setProperty('margin', 0)
        box.addStretch(1)
        self.setLayout(box)
        self.resize(150, 0)
        
    def hello(self):
        print "Hello World!"
        
    def error(self):
        raise Error("Error!")
        
    def quit(self):
        QCoreApplication.instance().quit()