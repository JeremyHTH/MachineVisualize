import sys,time,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from Componment import MovingComponent
import subprocess
import platform

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

class CenterWidget(QWidget):
    def __init__(self):
        super().__init__()


        self.init_UI()
        

    def init_UI(self):
        self.layout = QGridLayout(self)

        self.MidLayerDisplay = QLabel()
        canvas = QPixmap(WINDOW_WIDTH,WINDOW_HEIGHT)
        canvas.fill(Qt.black)
        self.MidLayerDisplay.setPixmap(canvas)
        self.layout.addWidget(self.MidLayerDisplay, 0, 0, 1, 1)

        self.DrawMidLayComponent()

        self.setLayout(self.layout)
    
    def DrawMidLayComponent(self):
        painter = QPainter(self.MidLayerDisplay.pixmap())
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor("#0a0838"))
        painter.setPen(pen)

        brush = QBrush()
        brush.setColor(QColor("#0a0838"))
        brush.setStyle(Qt.Dense1Pattern)
        painter.setBrush(brush)

        painter.drawRect(100,100,50,50)
        

    def close(self) -> bool:
        self.FirstRow.close()
        return super().close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.CenterWid = CenterWidget()
        self.setGeometry(1,90,800,600)
        self.setWindowTitle("Control Center")
        self.setCentralWidget(self.CenterWid)
        self.status = QStatusBar(self)
        self.status.showMessage("Welcome")
        self.setStatusBar(self.status)

        self.setStyle(QStyleFactory.create('fusion'))
        self.setStyleSheet(self.LoadStyle())

    def LoadStyle(self):
        data = ""
        try:
            with open('MainWindow.css','r') as f: 
                data = f.read()
        except Exception as e:
            print(e.args)
            # QMessageBox.question(self,'Error',str(e))
        return data
    
    def close(self) -> bool:
        self.CenterWid.close()
        return super().close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    container = MainWindow()

    container.show()
    sys.exit(app.exec_())