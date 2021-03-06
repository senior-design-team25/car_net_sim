import sys
import io
from time import time, sleep
from functools import partial

from config import global_config as config
from vmath import *
from map import Map

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtOpenGL import *



HANDLE_STYLE = """
QSplitter::handle:horizontal {
    background-color: qlineargradient(spread:pad, 
        x1:0, y1:0, x2:1, y2:0, 
        stop:0.0 rgba(200, 200, 200, 0),
        stop:0.1 rgba(100, 100, 100, 255), 
        stop:0.6 rgba(255, 255, 255, 0));
}

QSplitter::handle:vertical {
    background-color: qlineargradient(spread:pad, 
        x1:0, y1:0, x2:0, y2:1,
        stop:0.0 rgba(200, 200, 200, 0),
        stop:0.1 rgba(100, 100, 100, 255), 
        stop:0.6 rgba(255, 255, 255, 0));
}
"""


class SimConsole(QTextEdit):
    def __init__(self):
        super(SimConsole, self).__init__()        
        
        self.setReadOnly(True)
        
    def write(self, data):
        self.insertPlainText(data)
        self.ensureCursorVisible()
        
        
class SimScene(QGraphicsView):
    def __init__(self, map):
        super(SimScene, self).__init__()
        
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 100, 100)
        self.scale(self.width()/100.0, self.width()/100.0)
        
        self.scene.addItem(map.graphic)
        
        self.setScene(self.scene)
        self.setStyleSheet('background: black; border: 0')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setViewport(QGLWidget())
        
    def mousePressEvent(self, event):
        if not (Qt.LeftButton & event.buttons()) and \
           (Qt.MidButton | Qt.RightButton) & event.buttons():
            self.mouse = event.pos()
        
    def mouseMoveEvent(self, event):
        if not (Qt.LeftButton & event.buttons()) and \
           (Qt.MidButton | Qt.RightButton) & event.buttons():
            mouse = event.pos()
            delta = mouse - self.mouse
            self.mouse = mouse
            
            hbar = self.horizontalScrollBar()
            vbar = self.verticalScrollBar()
            hbar.setValue(hbar.value() - delta.x())
            vbar.setValue(vbar.value() - delta.y())
        
    def wheelEvent(self, event):
        hbar = self.horizontalScrollBar()
        vbar = self.verticalScrollBar()
        pos = QPointF(hbar.value(), vbar.value()) + event.pos()
        
        if event.delta() > 0:
            scale = 1.2
        else:
            scale = 1/1.2
            
        self.scale(scale, scale)
        pos = scale*pos - event.pos()
        
        hbar.setValue(pos.x())
        vbar.setValue(pos.y())
      
        
class SimControl(QWidget):
    def __init__(self, map, timeout, out):
        super(SimControl, self).__init__()
        self.timeout = timeout
        self.map = map
        self.out = out
        
        box = QVBoxLayout()
        
        reset = QPushButton('Reset')
        reset.clicked.connect(self.reset)
        
        box.addWidget(reset)
        
        self.time = QLabel()
        box.addWidget(self.time)
        self.vehicles = QLabel()
        box.addWidget(self.vehicles)
        self.messages = QLabel()
        box.addWidget(self.messages)
        self.collisions = QLabel()
        box.addWidget(self.collisions)
        
        cbox = QHBoxLayout()
        load = QPushButton('Load')
        load.clicked.connect(config.load)
        cbox.addWidget(load)
        save = QPushButton('Save')
        save.clicked.connect(config.dump)
        cbox.addWidget(save)
        box.addLayout(cbox)
        
        for key in config:
            label = QLabel(key)
            box.addWidget(label)
            input = QLineEdit(repr(config[key]))
            input.returnPressed.connect(partial(self.mod, key, input))
            box.addWidget(input)
        
        box.setProperty('spacing', 0)
        box.setProperty('margin', 0)
        box.addStretch(1)
        self.setLayout(box)
        self.resize(150, 0)
        
    def mod(self, key, input):
        config.eval(key, input.text())
        
    def reset(self):
        self.map.reset()
            
    def update(self):
        if self.map.time > self.timeout:
            self.out.write('Time: %0.3fs\n' % self.map.time)
            self.out.write('Collisions: %d\n' % self.map.collisions)
            self.out.flush()
            sys.exit(0)
    
        self.time.setText('Time: %0.3fs' % self.map.time)
        self.vehicles.setText('Vehicles: %d' % len(self.map.vehicles))
        self.messages.setText('Messages: %d' % sum(len(v.messages) for v in self.map.vehicles))
        self.collisions.setText('Collisions: %d' % self.map.collisions)
        
        

class CarNetSim(QWidget):
    def __init__(self, timeout):
        super(CarNetSim, self).__init__()
        
        self.map = Map()
        
        box = QHBoxLayout()
        
        self.console = SimConsole()
        self.scene = SimScene(self.map)
        self.control = SimControl(self.map, timeout, sys.stdout)
        
        self.timer = QBasicTimer()
        self.time = time()
        
        sys.stdout = self.console
        
        hw = QSplitter(Qt.Horizontal)
        vw = QSplitter(Qt.Vertical)
        
        box.addWidget(hw)
        hw.addWidget(vw)
        vw.addWidget(self.scene)
        vw.addWidget(self.console)
        hw.addWidget(self.control)
        
        hw.setStretchFactor(0, 1)
        hw.setStretchFactor(1, 0)
        vw.setStretchFactor(0, 1)
        vw.setStretchFactor(1, 0)
        
        hw.setSizes([800-150, 150])
        vw.setSizes([600-100, 100])
        
        box.setProperty('spacing', 0)
        box.setProperty('margin', 0)
        self.setLayout(box)
        self.setStyleSheet(HANDLE_STYLE)
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('Car Network Simulator')
        
    def show(self):
        self.timer.start(1000/60, self)
        
        super(CarNetSim, self).show()
        
    def timerEvent(self, event):
        ntime = time()
        dt = ntime - self.time
        self.time = ntime
        
        self.map.step(1.0/(60.0))
        self.control.update()

        
def main():
    root = QApplication(sys.argv)
    sim = CarNetSim(float(sys.argv[1] if len(sys.argv) >= 2 else 'inf'))
    sim.show()
    sys.exit(root.exec_())
    
if __name__ == '__main__':
    main()