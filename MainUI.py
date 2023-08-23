import sys,time,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect
from Componment import MovingComponent, Coordinate
import socket
import subprocess
import platform
import csv, yaml

import threading
HOST = socket.gethostname()
PORT = 9086

SIDE_WINDOW_WIDTH = 600
SIDE_WINDOW_HEIGHT = 800
MID_WINDOW_WIDTH = 600
MID_WINDOW_HEIGHT = 400
LOW_WINDOW_WIDTH = 600
LOW_WINDOW_HEIGHT = 400
VIEW_SETTING = {'Side': ("Head", "Eye", "MegaEye", "LeftLeg", "RightLeg"), 'Mid': ("Eye", "MegaEye", "Arm"), 'Bottom': ("LeftLeg", "RightLeg")}


class CenterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.ComponentList : dict[str, MovingComponent]= {}
        self.CreateComponent()
        self.ComponentDrawer = {'Pen': QPen(),'Brush': QBrush()}
        self.ComponentDrawer['Pen'].setWidth(1)
        self.ComponentDrawer['Pen'].setColor(QColor("#420803"))
        self.ComponentDrawer['Brush'].setColor(QColor("#0a0838"))
        self.ComponentDrawer['Brush'].setStyle(Qt.Dense1Pattern)
    
        self.TextDrawer = {'Pen': QPen(),'Brush': QBrush()}
        self.TextDrawer['Pen'].setWidth(1)
        self.TextDrawer['Pen'].setColor(QColor("#FFFFFF"))
        self.TextDrawer['Brush'].setColor(QColor("#FFFFFF"))
        self.TextDrawer['Brush'].setStyle(Qt.Dense1Pattern)

        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((HOST, PORT))
        self.Socket.settimeout(1)
        self.ConnectionContinue = False
        
        self.init_UI()
        
        
    def CreateComponent(self):
        self.ComponentList : dict[str, MovingComponent] = {}
        # with open("Configure/ComponentConfig.csv", 'r') as CSVFile:
        #     CSVRows = csv.reader(CSVFile)
        #     for Line in CSVRows:
        #         if (len(Line) >= 2 and Line[1] == '1'):
        #             self.ComponentList[Line[0]] = MovingComponent(Name = Line[0])
        #             if (len(Line) >= 5):
        #                 self.ComponentList[Line[0]].Dimension.x = eval(Line[2])
        #                 self.ComponentList[Line[0]].Dimension.y = eval(Line[3])
        #                 self.ComponentList[Line[0]].Dimension.z = eval(Line[4])
        
        # if ('Eye' in self.ComponentList):
        #     self.ComponentList['Eye'].CurrPos = Coordinate(200, 200, 450)
        # if ('MegaEye' in self.ComponentList):    
        #     self.ComponentList['MegaEye'].CurrPos = Coordinate(100, 100, 450)
        # if ('Head' in self.ComponentList):    
        #     self.ComponentList['Head'].CurrPos = Coordinate(250, 100, 0)
        # if ('LeftLeg' in self.ComponentList):    
        #     self.ComponentList['LeftLeg'].CurrPos = Coordinate(100, 100, 700)
        # if ('RightLeg' in self.ComponentList):    
        #     self.ComponentList['RightLeg'].CurrPos = Coordinate(500, 100, 700)

        with open("Configure/ComponentConfig.yml",'r') as f:
            Data = yaml.safe_load(f)

            for key, Detail in Data.items():
                print(key, Detail)
                self.ComponentList[key] = MovingComponent(Name = key, **Detail)
        print(self.ComponentList)
    def init_UI(self):
        self.layout = QGridLayout(self)

        self.SideLayerDisplay = QLabel(self)
        self.SideCanvas = QPixmap(SIDE_WINDOW_WIDTH, SIDE_WINDOW_HEIGHT)
        self.SideLayerDisplay.setPixmap(self.SideCanvas)
        self.layout.addWidget(self.SideLayerDisplay, 0, 0, 2, 3)

        self.MidLayerDisplay = QLabel(self)
        self.MidCanvas = QPixmap(MID_WINDOW_WIDTH, MID_WINDOW_HEIGHT)
        self.MidLayerDisplay.setPixmap(self.MidCanvas)
        self.layout.addWidget(self.MidLayerDisplay, 0, 3, 1, 3)

        self.BottomLayerDisplay = QLabel(self)
        self.BottomCanvas = QPixmap(LOW_WINDOW_WIDTH, LOW_WINDOW_HEIGHT)
        self.BottomLayerDisplay.setPixmap(self.BottomCanvas)
        self.layout.addWidget(self.BottomLayerDisplay, 1, 3, 1, 3)

        self.TestMoveButton = QPushButton("Left", self)
        self.TestMoveButton.clicked.connect(self.TestMove)
        self.layout.addWidget(self.TestMoveButton, 2, 0, 1, 1)
        
        self.StartListeningButton = QPushButton("Start Listening",self)
        self.StartListeningButton.clicked.connect(self._StartServerListening)
        self.layout.addWidget(self.StartListeningButton, 2, 1, 1, 1)

        self.StopListeningButton = QPushButton("Stop Listening",self)
        self.StopListeningButton.clicked.connect(self._StopServerListening)
        self.layout.addWidget(self.StopListeningButton, 2, 2, 1, 1)

        self.DrawSideLayerComponent()
        self.DrawMidLayComponent()
        self.DrawBottomLayComponent()

        
        # self.setLayout(self.layout)

    def ConnectionHandler(conn, addr):
        print(f"Connected by {addr}")
        with conn:
            while(data := conn.recv(1024).decode()):
                # print("Entered")
                Pos = yaml.safe_load(data)
                print(Pos)
                conn.send(b"Received")
            print("Disconnect")

    def _StartServerListening(self):
        self.Socket.listen()

        self.ThreadList = []
        
        while self.ConnectionContinue:
            conn, addr = self.Socket.accept()
            NewThread = threading.Thread(target=self.ConnectionHandler, args=(conn, addr))
            # print(f"Connected by {addr}")
            # with conn:
            #     while(data := conn.recv(1024).decode()):
            #         # print("Entered")
            #         Pos = yaml.safe_load(data)
            #         print(Pos)
            #         conn.send(b"Received")

            #     print("Disconnect")
            NewThread.start()

    def _StopServerListening(self):
        self.ConnectionContinue = False




    def TestMove(self):

        for key in self.ComponentList.keys():
            self.ComponentList[key].CurrPos.x += 100
            self.ComponentList[key].CurrPos.y += 100
            self.ComponentList[key].CurrPos.z += 100
            print("Test", self.ComponentList[key].Name)
        self.DrawSideLayerComponent()
        self.DrawMidLayComponent()
        self.DrawBottomLayComponent()

    def DrawSideLayerComponent(self):
        canvas = QPixmap(SIDE_WINDOW_WIDTH, SIDE_WINDOW_HEIGHT)
        self.SideLayerDisplay.setPixmap(canvas)
        self.SideLayerDisplay.pixmap().fill(Qt.black)
        painter = QPainter(self.SideLayerDisplay.pixmap())

        for Component in VIEW_SETTING["Side"]:
            if (Component in self.ComponentList):
                Curr = self.ComponentList[Component]
                Rect = QRect(Curr.CurrPos.x, Curr.CurrPos.z, Curr.Dimension.x, Curr.Dimension.z)
                painter.setPen(self.ComponentDrawer['Pen'])
                painter.setBrush(self.ComponentDrawer['Brush'])
                painter.drawRect(Rect)
                painter.setPen(self.TextDrawer['Pen'])
                painter.setBrush(self.TextDrawer['Brush'])
                print(Curr.Name)
                painter.drawText(Rect, Qt.AlignCenter, Curr.Name)

    def DrawMidLayComponent(self):
        canvas = QPixmap(MID_WINDOW_WIDTH, MID_WINDOW_HEIGHT)
        self.MidLayerDisplay.setPixmap(canvas)
        self.MidLayerDisplay.pixmap().fill(Qt.black)
        painter = QPainter(self.MidLayerDisplay.pixmap())      
        

        for Component in VIEW_SETTING["Mid"]:
            if (Component in self.ComponentList):
                Curr = self.ComponentList[Component]
                Rect = QRect(int(Curr.CurrPos.x), int(Curr.CurrPos.y), int(Curr.Dimension.x), int(Curr.Dimension.y))
                painter.setPen(self.ComponentDrawer['Pen'])
                painter.setBrush(self.ComponentDrawer['Brush'])
                painter.drawRect(Rect)
                painter.setPen(self.TextDrawer['Pen'])
                painter.setBrush(self.TextDrawer['Brush'])
                print(Curr.Name)
                painter.drawText(Rect, Qt.AlignCenter, Curr.Name)
    
    def DrawBottomLayComponent(self):
        canvas = QPixmap(LOW_WINDOW_WIDTH, LOW_WINDOW_HEIGHT)
        self.BottomLayerDisplay.setPixmap(canvas)
        self.BottomLayerDisplay.pixmap().fill(Qt.black)
        painter = QPainter(self.BottomLayerDisplay.pixmap())      
        

        for Component in VIEW_SETTING["Bottom"]:
            if (Component in self.ComponentList):
                Curr = self.ComponentList[Component]
                Rect = QRect(Curr.CurrPos.x, Curr.CurrPos.y, Curr.Dimension.x, Curr.Dimension.y)
                painter.setPen(self.ComponentDrawer['Pen'])
                painter.setBrush(self.ComponentDrawer['Brush'])
                painter.drawRect(Rect)
                painter.setPen(self.TextDrawer['Pen'])
                painter.setBrush(self.TextDrawer['Brush'])
                print(Curr.Name)
                painter.drawText(Rect, Qt.AlignCenter, Curr.Name)

    def close(self) -> bool:
        self.FirstRow.close()
        self.Socket.close()
        return super().close()
    
    def __del__(self):
        print("delete")
        # self.FirstRow.close()
        self.Socket.close()
        # return super().close()

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