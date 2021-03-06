from PyQt4.QtGui import QMainWindow, QFileDialog, QLabel, QWidget, QPixmap, QIcon
from PyQt4.QtGui import QPushButton, QFont, QMessageBox, QDesktopWidget, QGraphicsOpacityEffect
from PyQt4.QtGui import QGraphicsBlurEffect
from PyQt4.QtCore import Qt, QSize, QTimer, QPropertyAnimation ,QStateMachine, QState, QPointF
from PyQt4.QtCore import QParallelAnimationGroup, QSequentialAnimationGroup, QEasingCurve
from PyQt4.QtCore import QPoint , QThread
from os import path, walk
import shutil
from array import array
from Tools import Opacity, Shadow, newOrder
import requests
from datetime import datetime
from math import sin
import urllib3
from telegram import ReplyKeyboardMarkup, Bot
from telegram.error import NetworkError, Unauthorized
import pygame
from time import sleep
# ! from picamera import PiCamera
# ! import RPi.GPIO as GPIO

def GPIOsetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(27,GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.setup(22,GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.setup(6,GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.setup(16,GPIO.IN)

update_id = None
MAJN_ID = 577321253
Father_ID = 1288912519
Mother_ID = 518708663
Alirezaishisname = 7141423261
bot = Bot(token='Your Telegram Token', base_url="https://tapi.bale.ai/")
OWM_token = 'Your openweathermap Token'
home_markup = ReplyKeyboardMarkup(keyboard=[
    ['🎛️ Room 🎛️', '📊 Info 📊'],
    ['⏭', '⏯','⏮'],
    ['📸','🔇', '🔊'],
    ['⚙ Setting ⚙']])
room_markup = ReplyKeyboardMarkup(keyboard=[
    ['💡', '🎧'],
    ['🔌', '🕯️'],
    ['🔒️', '🤖'],
    ['🏠 Home 🏠']])
setting_markup = ReplyKeyboardMarkup(keyboard=[
    ['⏰ Alarm ⏰'],
    ['🕋 Sobh 🕋️'],
    ['🕋 Zohr 🕋️'],
    ['🕋 Maghreb 🕋'],
    ['🏠 Home 🏠']])

class SyntaxUI(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        if ("Ui Setup" is not None):
            self.setObjectName("Syntax")
            self.resize(1024, 600)
            self.setMinimumSize(1024, 600)
            self.setMaximumSize(1024, 600)
            self.setWindowTitle("3MAJN5")
            self.setWindowFlags(Qt.FramelessWindowHint)
            if (path.exists('Label')):
                print("We have Label")
            else:
                src = str(
                    QFileDialog.getExistingDirectory(self, "Select a folder for Labels", "Label Folder"))
                dest = "Label"
                destination = shutil.copytree(src, dest)
        if ("AI" is not None):
            self.ANNLamp = 0
            self.AlarmPlaying = False
            self.ANNHT = 0
            self.Volume = 1
            self.randh = 0
            self.ANNZ = 50
            self.ANNH = array('f', (0 for i in range(0, 24)))
            for i in range(24):
                if (i < 6):
                    self.ANNH[i] = 20
                elif (i < 18):
                    self.ANNH[i] = 40
                else:
                    self.ANNH[i] = 50
        if ("BackGround" is not None):
            self.BGLabel1 = QLabel(self)
            self.BGLabel1.setGeometry(0, 0, 1024, 600)
            self.BGLabel2 = QLabel(self)
            self.BGLabel2.setGeometry(0, 0, 1024, 600)

            try:
                fileCheck1 = open("BGPath.txt", 'r')
                self.BGPath = fileCheck1.read()
                print(self.BGPath)
                self.BGPathL = []
                self.BGImagesNUM = 0
                for (self.dirpath, self.dirnames, self.filenames) in walk(self.BGPath):
                    print(len(self.filenames))
                    print(self.dirpath)
                    self.BGPathL.extend(self.filenames)
                    break
                self.BGLabel2.setPixmap(QPixmap(self.BGPath + self.BGPathL[self.BGImagesNUM]))
                print(self.BGPath + self.BGPathL[self.BGImagesNUM])
                self.BGLabel2.setStyleSheet("background:black")
            except:
                self.BGPath = str(QFileDialog.getExistingDirectory(self, "Select a folder for BackGround Images:",
                                                                   "Background Folder"))
                self.BGPath = self.BGPath.replace('\\', '/')
                self.BGPath += '/'
                print(self.BGPath)
                fileCheck1 = open("BGPath.txt", "w")
                fileCheck1.write(self.BGPath)
                fileCheck1.close()
                self.BGPathL = []
                self.BGImagesNUM = 0
                for (self.dirpath, self.dirnames, self.filenames) in walk(self.BGPath):
                    print(len(self.filenames))
                    print(self.dirpath)
                    self.BGPathL.extend(self.filenames)
                    break
                self.BGLabel2.setPixmap(QPixmap(self.BGPath + self.BGPathL[self.BGImagesNUM]))
                print(self.BGPath + self.BGPathL[self.BGImagesNUM])
                self.BGLabel2.setStyleSheet("background:black")
        if ("Music" is not None):
            try:
                fileCheck1 = open("MusicPath.txt", 'r')
                self.MusicPath = fileCheck1.read()
            except:
                self.MusicPath = str(
                    QFileDialog.getExistingDirectory(self, "Select a folder for Music", "Music Folder"))
                self.MusicPath = self.MusicPath.replace('\\', '/')
                self.MusicPath += '/'
                fileCheck1 = open("MusicPath.txt", "w")
                fileCheck1.write(self.MusicPath)
                fileCheck1.close()
            try:
                fileCheck1 = open("AlarmPath.txt", 'r')
                self.AlarmPath = fileCheck1.read()
            except:
                self.AlarmPath = QFileDialog.getOpenFileName(self, "Open a mp3 file for alarm", "Alarm mp3", " (*.mp3)")
                self.AlarmPath = self.AlarmPath.replace('\\', '/')
                fileCheck1 = open("AlarmPath.txt", "w")
                fileCheck1.write(self.AlarmPath)
                fileCheck1.close()
            try:
                fileCheck1 = open("Azan.txt", 'r')
                self.Azan = fileCheck1.read()
            except:
                self.Azan = QFileDialog.getOpenFileName(self, "Open a mp3 file for Azan", "Azan mp3", " (*.mp3)")
                self.Azan = self.Azan.replace('\\', '/')
                fileCheck1 = open("Azan.txt", "w")
                fileCheck1.write(self.Azan)
                fileCheck1.close()
            self.AzanPlaying = False
            self.AzanSobh = True
            self.AzanZohr = True
            self.AzanMaghreb = True
            print(self.MusicPath)
            self.MusicPathL = []
            self.MusicsNUM = 0
            self.MusicNumPlaying = 0
            self.MusicNormalMode = True
            self.MusicVolume = 0.1
            # self.SetVolume(0.1)
            self.MusicPlaying = False
            self.Musicdirpath = ""
            self.Musicdirnames = ""
            self.MusicFileName = ""
            for (self.Musicdirpath, self.Musicdirnames, self.MusicFileName) in walk(self.MusicPath):
                self.MusicsNUM = len(self.MusicFileName)
                self.MusicPathL.extend(self.MusicFileName)
                break
        if ("MenuButton" is not None):
            self.MenuWidget = QWidget(self)
            self.MenuWidget.setGeometry(0, 50, 80, 500)

            self.MenuLabel1 = QLabel(self.MenuWidget)
            self.MenuLabel1.setPixmap(QPixmap("Label/Menu/Menu.png"))
            self.MenuLabel1.setGeometry(0, 0, 80, 500)
            self.MenuLabel1.setGraphicsEffect(Opacity(0.7))

            self.MenuHomeBTN = QPushButton(self.MenuWidget)
            self.MenuHomeBTN.setIcon(QIcon("Label/Menu/HomeBTN.png"))
            self.MenuHomeBTN.setIconSize(QSize(50, 50))
            self.MenuHomeBTN.setGeometry(15, 20, 50, 50)
            self.MenuHomeBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MenuHomeBTN.setGraphicsEffect(Opacity(0.7))
            self.MenuHomeBTN.clicked.connect(self.MenuHomeBTNDef)

            self.MenuRoomBTN = QPushButton(self.MenuWidget)
            self.MenuRoomBTN.setIcon(QIcon("Label/Menu/RoomBTN.png"))
            self.MenuRoomBTN.setIconSize(QSize(50, 50))
            self.MenuRoomBTN.setGeometry(15, 100, 50, 50)
            self.MenuRoomBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MenuRoomBTN.setGraphicsEffect(Opacity(0.7))
            self.MenuRoomBTN.clicked.connect(self.MenuRoomBTNDef)

            self.MenuTempBTN = QPushButton(self.MenuWidget)
            self.MenuTempBTN.setIcon(QIcon("Label/Menu/TempBTN.png"))
            self.MenuTempBTN.setIconSize(QSize(50, 50))
            self.MenuTempBTN.setGeometry(15, 180, 50, 50)
            self.MenuTempBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MenuTempBTN.setGraphicsEffect(Opacity(0.7))
            self.MenuTempBTN.clicked.connect(self.MenuTempBTNDef)

            self.MenuMusicBTN = QPushButton(self.MenuWidget)
            self.MenuMusicBTN.setIcon(QIcon("Label/Menu/MusicBTN.png"))
            self.MenuMusicBTN.setIconSize(QSize(50, 50))
            self.MenuMusicBTN.setGeometry(15, 260, 50, 50)
            self.MenuMusicBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MenuMusicBTN.setGraphicsEffect(Opacity(0.7))
            self.MenuMusicBTN.clicked.connect(self.MenuMusicBTNDef)

            self.MenuBaleBTN = QPushButton(self.MenuWidget)
            self.MenuBaleBTN.setIcon(QIcon("Label/Menu/BaleBTN.png"))
            self.MenuBaleBTN.setIconSize(QSize(50, 50))
            self.MenuBaleBTN.setGeometry(15, 340, 50, 50)
            self.MenuBaleBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MenuBaleBTN.setGraphicsEffect(Opacity(0.7))
            self.MenuBaleBTN.clicked.connect(self.MenuBaleBTNDef)

            self.MenuSetBTN = QPushButton(self.MenuWidget)
            self.MenuSetBTN.setIcon(QIcon("Label/Menu/SetBTN.png"))
            self.MenuSetBTN.setIconSize(QSize(50, 50))
            self.MenuSetBTN.setGeometry(15, 420, 50, 50)
            self.MenuSetBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MenuSetBTN.setGraphicsEffect(Opacity(0.7))
            self.MenuSetBTN.clicked.connect(self.MenuSetBTNDef)
        if ("HomeTab" is not None):
            self.HomeTabWidget = QWidget(self)
            self.HomeTabWidget.setGeometry(774, 50, 250, 500)
            self.HomeTabLabel = QLabel(self.HomeTabWidget)
            self.HomeTabLabel.setPixmap(QPixmap("Label/HomeTabLabel1.png"))
            self.HomeTabLabel.setGeometry(0, 0, 250, 500)
            self.HomeTabLabel.setGraphicsEffect(Opacity(0.5))
            '''------------------------------------------------------------------------------------------------------'''
            self.HomeTabDay = QLabel(self.HomeTabWidget)
            self.HomeTabDay.setGeometry(10, 15, 220, 50)
            self.HomeTabDay.setText("Saturday")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(36)
            self.HomeTabDay.setFont(self.EbrimaFont)
            self.HomeTabDay.setAlignment(Qt.AlignCenter)
            self.HomeTabDay.setStyleSheet('color:white;')
            self.HomeTabDay.setGraphicsEffect(Opacity(0.7))

            self.HomeTabDate = QLabel(self.HomeTabWidget)
            self.HomeTabDate.setGeometry(10, 60, 220, 50)
            self.HomeTabDate.setText("23 June 2018")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(20)
            self.HomeTabDate.setFont(self.EbrimaFont)
            self.HomeTabDate.setAlignment(Qt.AlignCenter)
            self.HomeTabDate.setStyleSheet('color:white;')
            self.HomeTabDate.setGraphicsEffect(Opacity(0.7))
            '''------------------------------------------------------------------------------------------------------'''
            self.HomeTabWeatherWidget = QWidget(self.HomeTabWidget)
            self.HomeTabWeatherWidget.setGeometry(0, 122, 250, 90)
            self.HomeTabWeatherWidget.setStyleSheet("background:url(\"Label/HomeTabLabel2.png\");")
            self.HomeTabWeatherWidget.setGraphicsEffect(Opacity(0.5))
            global OWM_token
            r = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=Tehran&APPID='+OWM_token)
            self.OutsideTempW = str(int(r.json()['main']['temp']) - 273.15)
            self.OutSideHumidityW = str(r.json()['main']['humidity'])
            self.HomeTabWeatherLabel = QLabel(self.HomeTabWeatherWidget)
            self.HomeTabWeatherLabel.setGeometry(0, 0, 250, 85)
            self.HomeTabWeatherLabel.setText(str(r.json()['weather'][0]['description']))
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(35 - (0.7 * len(str(r.json()['weather'][0]['description']))))
            self.HomeTabWeatherLabel.setFont(self.EbrimaFont)
            self.HomeTabWeatherLabel.setAlignment(Qt.AlignCenter)
            self.HomeTabWeatherLabel.setStyleSheet('color:white;')
            self.HomeTabWeatherLabel.setGraphicsEffect(Opacity(1))
            '''------------------------------------------------------------------------------------------------------'''
            self.HomeTabClockWidget = QWidget(self.HomeTabWidget)
            self.HomeTabClockWidget.setGeometry(20, 220, 210, 60)

            self.HomeTabClockOO1 = QPushButton(self.HomeTabClockWidget)
            self.HomeTabClockOO1.setIcon(QIcon("Label/Circle.png"))
            self.HomeTabClockOO1.setIconSize(QSize(12, 12))
            self.HomeTabClockOO1.setGeometry(60, 9, 12, 12)
            self.HomeTabClockOO1.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.HomeTabClockOO1.setGraphicsEffect(Opacity(0.6))

            self.HomeTabClockOO2 = QPushButton(self.HomeTabClockWidget)
            self.HomeTabClockOO2.setIcon(QIcon("Label/Circle.png"))
            self.HomeTabClockOO2.setIconSize(QSize(12, 12))
            self.HomeTabClockOO2.setGeometry(60, 40, 12, 12)
            self.HomeTabClockOO2.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.HomeTabClockOO2.setGraphicsEffect(Opacity(0.6))

            self.HomeTabClockOO3 = QPushButton(self.HomeTabClockWidget)
            self.HomeTabClockOO3.setIcon(QIcon("Label/Circle.png"))
            self.HomeTabClockOO3.setIconSize(QSize(12, 12))
            self.HomeTabClockOO3.setGeometry(138, 9, 12, 12)
            self.HomeTabClockOO3.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.HomeTabClockOO3.setGraphicsEffect(Opacity(0.6))

            self.HomeTabClockOO4 = QPushButton(self.HomeTabClockWidget)
            self.HomeTabClockOO4.setIcon(QIcon("Label/Circle.png"))
            self.HomeTabClockOO4.setIconSize(QSize(12, 12))
            self.HomeTabClockOO4.setGeometry(138, 40, 12, 12)
            self.HomeTabClockOO4.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.HomeTabClockOO4.setGraphicsEffect(Opacity(0.6))

            self.HomeTabClockH = QLabel(self.HomeTabClockWidget)
            self.HomeTabClockH.setGeometry(0, 10, 60, 40)
            self.HomeTabClockH.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabClockH.setText("6")
            self.HomeTabClockH.setGraphicsEffect(Opacity(0.7))
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(40)
            self.HomeTabClockH.setFont(self.EbrimaFont)
            self.HomeTabClockH.setAlignment(Qt.AlignCenter)

            self.HomeTabClockM = QLabel(self.HomeTabClockWidget)
            self.HomeTabClockM.setGeometry(75, 10, 60, 40)
            self.HomeTabClockM.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabClockM.setText("30")
            self.HomeTabClockM.setGraphicsEffect(Opacity(0.7))
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(40)
            self.HomeTabClockM.setFont(self.EbrimaFont)
            self.HomeTabClockM.setAlignment(Qt.AlignCenter)

            self.HomeTabClockS = QLabel(self.HomeTabClockWidget)
            self.HomeTabClockS.setGeometry(149, 10, 60, 40)
            self.HomeTabClockS.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabClockS.setText("15")
            self.HomeTabClockS.setGraphicsEffect(Opacity(0.7))
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(40)
            self.HomeTabClockS.setFont(self.EbrimaFont)
            self.HomeTabClockS.setAlignment(Qt.AlignCenter)
            '''------------------------------------------------------------------------------------------------------'''
            self.HomeTabTempWidget = QWidget(self.HomeTabWidget)
            self.HomeTabTempWidget.setGeometry(0, 288, 250, 90)
            self.HomeTabTempWidget.setStyleSheet("background:url(\"Label/HomeTabLabel2.png\");")
            self.HomeTabTempWidget.setGraphicsEffect(Opacity(0.5))

            self.HomeTabTText = QLabel(self.HomeTabTempWidget)
            self.HomeTabTText.setGeometry(0, 0, 250, 20)
            self.HomeTabTText.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabTText.setText("Inside")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(20)
            self.HomeTabTText.setFont(self.EbrimaFont)
            self.HomeTabTText.setAlignment(Qt.AlignCenter)

            self.HomeTabHumidityLabel = QLabel(self.HomeTabTempWidget)
            self.HomeTabHumidityLabel.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabHumidityLabel.setGeometry(40, 10, 70, 70)
            self.HomeTabHumidityLabel.setPixmap(QPixmap("Label/humidity.png"))
            self.HomeTabHumidityLabel.setAlignment(Qt.AlignLeft)
            self.HomeTabHumidityLabel.setGraphicsEffect(Opacity(0.35))
            self.HomeTabHumidityText = QLabel(self.HomeTabTempWidget)
            self.HomeTabHumidityText.setGeometry(5, 10, 70, 70)
            self.HomeTabHumidityText.setStyleSheet("background:url(\"\");color:white")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(40)
            self.HomeTabHumidityText.setFont(self.EbrimaFont)
            self.HomeTabHumidityText.setAlignment(Qt.AlignCenter)

            self.HomeTabTempLabel = QLabel(self.HomeTabTempWidget)
            self.HomeTabTempLabel.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabTempLabel.setGeometry(180, 10, 70, 70)
            self.HomeTabTempLabel.setPixmap(QPixmap("Label/temperature.png"))
            self.HomeTabTempLabel.setAlignment(Qt.AlignCenter)
            self.HomeTabTempLabel.setGraphicsEffect(Opacity(0.35))
            self.HomeTabTempText = QLabel(self.HomeTabTempWidget)
            self.HomeTabTempText.setGeometry(110, 10, 90, 70)
            self.HomeTabTempText.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabTempText.setText("25")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(40)
            self.HomeTabTempText.setFont(self.EbrimaFont)
            self.HomeTabTempText.setAlignment(Qt.AlignCenter)
            self.HomeTabTempLabelC = QLabel(self.HomeTabTempWidget)
            self.HomeTabTempLabelC.setStyleSheet("background:url(\"\");color:white")
            self.HomeTabTempLabelC.setGeometry(170, 22, 16, 16)
            self.HomeTabTempLabelC.setPixmap(QPixmap("Label/C.png"))
            self.HomeTabTempLabelC.setAlignment(Qt.AlignCenter)
            self.HomeTabTempLabelC.setGraphicsEffect(Opacity(0.65))
            self.WeatherCheckD = QTimer(self)
            self.WeatherCheckD.setInterval(60000)
            self.WeatherCheckD.timeout.connect(self.WeatherCheck)
            self.WeatherCheckD.start()
            '''------------------------------------------------------------------------------------------------------'''
            self.HomeTabMusicBack = QPushButton(self.HomeTabWidget)
            self.HomeTabMusicBack.setIcon(QIcon("Label/back.png"))
            self.HomeTabMusicBack.setIconSize(QSize(40, 40))
            self.HomeTabMusicBack.setGeometry(20, 419, 40, 40)
            self.HomeTabMusicBack.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.HomeTabMusicBack.setGraphicsEffect(Opacity(0.4))
            self.HomeTabMusicBack.clicked.connect(self.BackMusicDef)
            self.HomeTabMusicPlay = QPushButton(self.HomeTabWidget)
            self.HomeTabMusicPlay.setIcon(QIcon("Label/play.png"))
            self.HomeTabMusicPlay.setIconSize(QSize(80, 80))
            self.HomeTabMusicPlay.setGeometry(85, 399, 80, 80)
            self.HomeTabMusicPlay.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.HomeTabMusicPlay.setGraphicsEffect(Opacity(0.4))
            self.HomeTabMusicPlay.clicked.connect(self.PlayMusicDef)
            self.HomeTabMusicNext = QPushButton(self.HomeTabWidget)
            self.HomeTabMusicNext.setIcon(QIcon("Label/next.png"))
            self.HomeTabMusicNext.setIconSize(QSize(40, 40))
            self.HomeTabMusicNext.setGeometry(190, 419, 40, 40)
            self.HomeTabMusicNext.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.HomeTabMusicNext.setGraphicsEffect(Opacity(0.4))
            self.HomeTabMusicNext.clicked.connect(self.NextMusicDef)
        if ("RoomTab" is not None):
            self.RoomTabWidget = QWidget(self)
            self.RoomTabWidget.setGeometry(274, 50, 750, 500)
            self.RoomTabLabel = QLabel(self.RoomTabWidget)
            self.RoomTabLabel.setPixmap(QPixmap("Label/RoomLabel.png"))
            self.RoomTabLabel.setGeometry(0, 0, 750, 500)
            self.RoomTabLabel.setGraphicsEffect(Opacity(0.5))
            '''##############################################################################################LabelOFF'''
            self.RoomTabBTN1LabelOFF = QLabel(self.RoomTabWidget)
            self.RoomTabBTN1LabelOFF.setGeometry(117, 25, 200, 200)
            self.RoomTabBTN1LabelOFF.setPixmap(QPixmap("Label/OFFLabel1.png"))
            self.RoomTabBTN1LabelOFF.setGraphicsEffect(Opacity(0.6))
            self.RoomTabBTN2LabelOFF = QLabel(self.RoomTabWidget)
            self.RoomTabBTN2LabelOFF.setGeometry(434, 25, 200, 200)
            self.RoomTabBTN2LabelOFF.setPixmap(QPixmap("Label/OFFLabel1.png"))
            self.RoomTabBTN2LabelOFF.setGraphicsEffect(Opacity(0.6))
            self.RoomTabBTN3LabelOFF = QLabel(self.RoomTabWidget)
            self.RoomTabBTN3LabelOFF.setGeometry(117, 275, 200, 200)
            self.RoomTabBTN3LabelOFF.setPixmap(QPixmap("Label/OFFLabel1.png"))
            self.RoomTabBTN3LabelOFF.setGraphicsEffect(Opacity(0.6))
            self.RoomTabBTN4LabelOFF = QLabel(self.RoomTabWidget)
            self.RoomTabBTN4LabelOFF.setGeometry(434, 275, 200, 200)
            self.RoomTabBTN4LabelOFF.setPixmap(QPixmap("Label/OFFLabel1.png"))
            self.RoomTabBTN4LabelOFF.setGraphicsEffect(Opacity(0.6))
            '''##############################################################################################LabelON'''
            self.RoomTabBTN1LabelON = QLabel(self.RoomTabWidget)
            self.RoomTabBTN1LabelON.setGeometry(117, 25, 200, 200)
            self.RoomTabBTN1LabelON.setPixmap(QPixmap("Label/ONLabel1.png"))
            self.RoomTabBTN1LabelON.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN2LabelON = QLabel(self.RoomTabWidget)
            self.RoomTabBTN2LabelON.setGeometry(434, 25, 200, 200)
            self.RoomTabBTN2LabelON.setPixmap(QPixmap("Label/ONLabel1.png"))
            self.RoomTabBTN2LabelON.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN3LabelON = QLabel(self.RoomTabWidget)
            self.RoomTabBTN3LabelON.setGeometry(117, 275, 200, 200)
            self.RoomTabBTN3LabelON.setPixmap(QPixmap("Label/ONLabel1.png"))
            self.RoomTabBTN3LabelON.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN4LabelON = QLabel(self.RoomTabWidget)
            self.RoomTabBTN4LabelON.setGeometry(434, 275, 200, 200)
            self.RoomTabBTN4LabelON.setPixmap(QPixmap("Label/ONLabel1.png"))
            self.RoomTabBTN4LabelON.setGraphicsEffect(Opacity(0))
            '''################################################################################################Label2'''
            self.RoomTabBTN1Label2 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN1Label2.setGeometry(117, 25, 200, 200)
            self.RoomTabBTN1Label2.setPixmap(QPixmap("Label/BTN1/Label2.png"))
            self.RoomTabBTN1Label2.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN2Label2 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN2Label2.setGeometry(434, 25, 200, 200)
            self.RoomTabBTN2Label2.setPixmap(QPixmap("Label/BTN2/Label2.png"))
            self.RoomTabBTN2Label2.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN3Label2 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN3Label2.setGeometry(117, 275, 200, 200)
            self.RoomTabBTN3Label2.setPixmap(QPixmap("Label/BTN3/Label2.png"))
            self.RoomTabBTN3Label2.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN4Label2 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN4Label2.setGeometry(434, 275, 200, 200)
            self.RoomTabBTN4Label2.setPixmap(QPixmap("Label/BTN4/Label2.png"))
            self.RoomTabBTN4Label2.setGraphicsEffect(Opacity(0))
            '''################################################################################################Label3'''
            self.RoomTabBTN1Label3 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN1Label3.setGeometry(117, 25, 200, 200)
            self.RoomTabBTN1Label3.setPixmap(QPixmap("Label/BTN1/Label3.png"))
            self.RoomTabBTN1Label3.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN2Label3 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN2Label3.setGeometry(434, 25, 200, 200)
            self.RoomTabBTN2Label3.setPixmap(QPixmap("Label/BTN2/Label3.png"))
            self.RoomTabBTN2Label3.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN3Label3 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN3Label3.setGeometry(117, 275, 200, 200)
            self.RoomTabBTN3Label3.setPixmap(QPixmap("Label/BTN3/Label3.png"))
            self.RoomTabBTN3Label3.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN4Label3 = QLabel(self.RoomTabWidget)
            self.RoomTabBTN4Label3.setGeometry(434, 275, 200, 200)
            self.RoomTabBTN4Label3.setPixmap(QPixmap("Label/BTN4/Label3.png"))
            self.RoomTabBTN4Label3.setGraphicsEffect(Opacity(0))
            '''#############################################################################################InsideOff'''
            self.RoomTabBTN1OFF = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN1OFF.setGeometry(117, 25, 200, 200)
            self.RoomTabBTN1OFF.setIcon(QIcon("Label/BTN1/ImageOFF.png"))
            self.RoomTabBTN1OFF.setIconSize(QSize(200, 200))
            self.RoomTabBTN1OFF.setGraphicsEffect(Opacity(0.3))
            self.RoomTabBTN1OFF.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.RoomTabBTN2OFF = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN2OFF.setGeometry(434, 25, 200, 200)
            self.RoomTabBTN2OFF.setIcon(QIcon("Label/BTN2/ImageOFF.png"))
            self.RoomTabBTN2OFF.setIconSize(QSize(200, 200))
            self.RoomTabBTN2OFF.setGraphicsEffect(Opacity(0.3))
            self.RoomTabBTN2OFF.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.RoomTabBTN3OFF = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN3OFF.setGeometry(117, 275, 200, 200)
            self.RoomTabBTN3OFF.setIcon(QIcon("Label/BTN3/ImageOFF.png"))
            self.RoomTabBTN3OFF.setIconSize(QSize(200, 200))
            self.RoomTabBTN3OFF.setGraphicsEffect(Opacity(0.3))
            self.RoomTabBTN3OFF.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.RoomTabBTN4OFF = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN4OFF.setGeometry(434, 275, 200, 200)
            self.RoomTabBTN4OFF.setIcon(QIcon("Label/BTN4/ImageOFF.png"))
            self.RoomTabBTN4OFF.setIconSize(QSize(200, 200))
            self.RoomTabBTN4OFF.setGraphicsEffect(Opacity(0.3))
            self.RoomTabBTN4OFF.setStyleSheet("border-radius: 5%;outline-style: initial;")
            '''#############################################################################################InsideOn'''
            self.RoomTabBTN1ON = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN1ON.setGeometry(117, 25, 200, 200)
            self.RoomTabBTN1ON.setIcon(QIcon("Label/BTN1/ImageON.png"))
            self.RoomTabBTN1ON.setIconSize(QSize(200, 200))
            self.RoomTabBTN1ON.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN1ON.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.RoomTabBTN2ON = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN2ON.setGeometry(434, 25, 200, 200)
            self.RoomTabBTN2ON.setIcon(QIcon("Label/BTN2/ImageON.png"))
            self.RoomTabBTN2ON.setIconSize(QSize(200, 200))
            self.RoomTabBTN2ON.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN2ON.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.RoomTabBTN3ON = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN3ON.setGeometry(117, 275, 200, 200)
            self.RoomTabBTN3ON.setIcon(QIcon("Label/BTN3/ImageON.png"))
            self.RoomTabBTN3ON.setIconSize(QSize(200, 200))
            self.RoomTabBTN3ON.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN3ON.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.RoomTabBTN4ON = QPushButton(self.RoomTabWidget)
            self.RoomTabBTN4ON.setGeometry(434, 275, 200, 200)
            self.RoomTabBTN4ON.setIcon(QIcon("Label/BTN4/ImageON.png"))
            self.RoomTabBTN4ON.setIconSize(QSize(200, 200))
            self.RoomTabBTN4ON.setGraphicsEffect(Opacity(0))
            self.RoomTabBTN4ON.setStyleSheet("border-radius: 5%;outline-style: initial;")
            '''#################################################################################################Clock'''
            self.RoomTabClockH = QLabel(self.RoomTabWidget)
            self.RoomTabClockH.setGeometry(0, 200, 170, 100)
            self.RoomTabClockH.setText("19")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(110)
            self.RoomTabClockH.setFont(self.EbrimaFont)
            self.RoomTabClockH.setAlignment(Qt.AlignCenter)
            self.RoomTabClockH.setStyleSheet('color:white;')
            self.RoomTabClockH.setGraphicsEffect(Opacity(0.4))

            self.RoomTabClockM = QLabel(self.RoomTabWidget)
            self.RoomTabClockM.setGeometry(290, 200, 170, 100)
            self.RoomTabClockM.setText("30")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(110)
            self.RoomTabClockM.setFont(self.EbrimaFont)
            self.RoomTabClockM.setAlignment(Qt.AlignCenter)
            self.RoomTabClockM.setStyleSheet('color:white;')
            self.RoomTabClockM.setGraphicsEffect(Opacity(0.4))

            self.RoomTabClockS = QLabel(self.RoomTabWidget)
            self.RoomTabClockS.setGeometry(590, 200, 170, 100)
            self.RoomTabClockS.setText("15")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(110)
            self.RoomTabClockS.setFont(self.EbrimaFont)
            self.RoomTabClockS.setAlignment(Qt.AlignCenter)
            self.RoomTabClockS.setStyleSheet('color:white;')
            self.RoomTabClockS.setGraphicsEffect(Opacity(0.4))
        if ("TempCoTab" is not None):
            self.TempCoWidget = QWidget(self)
            self.TempCoWidget.setGeometry(474, 50, 550, 550)
            self.TempCoTabGraphWidget = QWidget(self.TempCoWidget)
            self.TempCoTabGraphWidget.setGeometry(0, 0, 550, 260)
            TempCoTabGraphWidget = QWidget(self.TempCoWidget)
            TempCoTabGraphWidget.setGeometry(0, 0, 550, 260)
            self.TempCoTabGraphLabell = QLabel(self.TempCoTabGraphWidget)
            self.TempCoTabGraphLabell.setGeometry(0, 0, 550, 260)
            self.TempCoTabGraphLabell.setPixmap(QPixmap("Label/TempCoLabel1.png"))
            self.TempCoTabGraphLabell.setGraphicsEffect(Opacity(0.7))
            self.TempCoSetStyleSheetL = "background:url(\"Label/GraphTempL.png\");"
            self.TempCoSetStyleSheetM = "background:url(\"Label/GraphTempM.png\");"
            self.TempCoSetStyleSheetH = "background:url(\"Label/GraphTempH.png\");"
            self.TempClockInHour = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.TempCoTabGraphH = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            self.TempCheck = QTimer(self)
            self.TempCheck.setInterval(1000)
            self.TempCheck.timeout.connect(self.TempCheckDef)
            self.TempCheck.start()
            self.TempCheckAve = 0
            now = datetime.now()

            for n in range(24):
                self.TempClockInHour[n] = 0.2 * (sin(n)) * n + 25
                self.TempCoTabGraphH[n] = QLabel(self.TempCoTabGraphWidget)
                self.TempCoTabGraphH[n].setGeometry(
                    53 + n * (454 / 23), 215 - ((self.TempClockInHour[n] - 19) * (185 / 12)), 10,
                    ((self.TempClockInHour[n] - 19) * (185 / 12)))
                if (self.TempClockInHour[n] <= 22.5):
                    self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetL)
                elif (self.TempClockInHour[n] < 27.5):
                    self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetM)
                else:
                    self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetH)
                self.TempCoTabGraphH[n].setGraphicsEffect(Opacity(0.4))

            # ! hm, tm = Adafruit_DHT.read_retry(22, 4)
            self.TempCheckAve = [22, 23]  # tm
            for n in range(24):
                if (n == int(now.hour) - 1):
                    self.TempClockInHour[n] = 0  # ! float(tm)
                    self.TempCoTabGraphH[n].setGeometry(
                        53 + n * (454 / 23), 215 - ((self.TempClockInHour[n] - 19) * (185 / 12)), 10,
                        ((self.TempClockInHour[n] - 19) * (185 / 12)))
                    if (self.TempClockInHour[n] <= 21):
                        self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetL)
                    elif (self.TempClockInHour[n] <= 27):
                        self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetM)
                    else:
                        self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetH)
                    self.TempCoTabGraphH[n].setGraphicsEffect(Opacity(0.4))

            if ("Auto" != None):
                self.TempCoTabAutoWidget = QWidget(self.TempCoWidget)
                self.TempCoTabAutoWidget.setGeometry(215, 300, 335, 150)

                self.TempCoTabAutoLabel = QLabel(self.TempCoTabAutoWidget)
                self.TempCoTabAutoLabel.setGeometry(0, 0, 335, 150)
                self.TempCoTabAutoLabel.setPixmap(QPixmap("Label/TempCoAutoWidgetLabel.png"))
                self.TempCoTabAutoLabel.setGraphicsEffect(Opacity(0.95))

                self.TempCoTabAutoOutsideTempLabel = QLabel(self.TempCoTabAutoWidget)
                self.TempCoTabAutoOutsideTempLabel.setGeometry(10, 43, 64, 64)
                self.TempCoTabAutoOutsideTempLabel.setPixmap(QPixmap("Label/TempCoTabAutoOutside.png"))
                self.TempCoTabAutoOutsideTempLabel.setGraphicsEffect(Opacity(0.3))
                self.TempCoTabAutoOutsideTempTXT = QLabel(self.TempCoTabAutoWidget)
                self.TempCoTabAutoOutsideTempTXT.setGeometry(10, 43, 64, 64)
                self.TempCoTabAutoOutsideTempTXT.setText("31")
                self.EbrimaFont = QFont()
                self.EbrimaFont.setFamily('Ebrima')
                self.EbrimaFont.setPixelSize(45)
                self.TempCoTabAutoOutsideTempTXT.setFont(self.EbrimaFont)
                self.TempCoTabAutoOutsideTempTXT.setAlignment(Qt.AlignCenter)
                self.TempCoTabAutoOutsideTempTXT.setStyleSheet('color:black;')
                self.TempCoTabAutoOutsideTempTXT.setGraphicsEffect(Opacity(0.7))

                self.TempCoTabAutoInsideTempLabel = QLabel(self.TempCoTabAutoWidget)
                self.TempCoTabAutoInsideTempLabel.setGeometry(80, 14, 125, 125)
                self.TempCoTabAutoInsideTempLabel.setPixmap(QPixmap("Label/TempCoTabAutoInside.png"))
                self.TempCoTabAutoInsideTempLabel.setGraphicsEffect(Opacity(0.3))
                self.TempCoTabAutoInsideTempTXT = QLabel(self.TempCoTabAutoWidget)
                self.TempCoTabAutoInsideTempTXT.setGeometry(80, 16, 125, 125)
                self.TempCoTabAutoInsideTempTXT.setText("25")
                self.EbrimaFont = QFont()
                self.EbrimaFont.setFamily('Ebrima')
                self.EbrimaFont.setPixelSize(70)
                self.TempCoTabAutoInsideTempTXT.setFont(self.EbrimaFont)
                self.TempCoTabAutoInsideTempTXT.setAlignment(Qt.AlignCenter)
                self.TempCoTabAutoInsideTempTXT.setStyleSheet('color:black;')
                self.TempCoTabAutoInsideTempTXT.setGraphicsEffect(Opacity(0.7))

                self.TempCoTabAutoUpBTN = QPushButton(self.TempCoTabAutoWidget)
                self.TempCoTabAutoUpBTN.setGeometry(170, 0, 60, 60)
                self.TempCoTabAutoUpBTN.setIcon(QIcon("Label/TempCoAutoUp.png"))
                self.TempCoTabAutoUpBTN.setIconSize(QSize(60, 60))
                self.TempCoTabAutoUpBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.TempCoTabAutoUpBTN.setGraphicsEffect(Opacity(0.5))
                self.TempCoTabAutoUpBTN.clicked.connect(self.TempCoTabAutoUpBTNDef)

                self.TempCoTabAutoDownBTN = QPushButton(self.TempCoTabAutoWidget)
                self.TempCoTabAutoDownBTN.setGeometry(170, 90, 60, 60)
                self.TempCoTabAutoDownBTN.setIcon(QIcon("Label/TempCoAutoDown.png"))
                self.TempCoTabAutoDownBTN.setIconSize(QSize(60, 60))
                self.TempCoTabAutoDownBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.TempCoTabAutoDownBTN.setGraphicsEffect(Opacity(0.5))
                self.TempCoTabAutoDownBTN.clicked.connect(self.TempCoTabAutoDownBTNDef)
            if ("Manual" != None):
                self.TempCoTabManualWidget = QWidget(self.TempCoWidget)
                self.TempCoTabManualWidget.setGeometry(550, 300, 300, 150)
                self.TempCoTabManualLabel = QLabel(self.TempCoTabManualWidget)
                self.TempCoTabManualLabel.setGeometry(0, 0, 300, 150)
                self.TempCoTabManualLabel.setPixmap(QPixmap("Label/TempCoManualLabel.png"))

                self.TempCoTabManualTurnLabel = QLabel(self.TempCoTabManualWidget)
                self.TempCoTabManualTurnLabel.setGeometry(125, 77, 50, 50)
                self.TempCoTabManualTurnLabel.setPixmap(QPixmap("Label/TempCoManualLabelBTN.png"))
                self.TempCoTabManualTurnLabel.setGraphicsEffect(Shadow(1, 1, 2, 2))
                self.TempCoTabManualTurn = QPushButton(self.TempCoTabManualWidget)
                self.TempCoTabManualTurn.setGeometry(120, 0, 72, 150)
                self.TempCoTabManualTurn.setIcon(QIcon(""))
                self.TempCoTabManualTurn.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.TempCoTabManualTurn.clicked.connect(self.TempCoTabManualTurnDef)
                self.TempCoTabManualTurnBool = False

                self.TempCoTabManualSpeedLabel = QLabel(self.TempCoTabManualWidget)
                self.TempCoTabManualSpeedLabel.setGeometry(29, 77, 50, 50)
                self.TempCoTabManualSpeedLabel.setPixmap(QPixmap("Label/TempCoManualLabelBTN.png"))
                self.TempCoTabManualSpeedLabel.setGraphicsEffect(Shadow(1, 1, 2, 2))
                self.TempCoTabManualSpeed = QPushButton(self.TempCoTabManualWidget)
                self.TempCoTabManualSpeed.setGeometry(20, 0, 72, 150)
                self.TempCoTabManualSpeed.setIcon(QIcon(""))
                self.TempCoTabManualSpeed.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.TempCoTabManualSpeed.clicked.connect(self.TempCoTabManualSpeedDef)
                self.TempCoTabManualSpeedBool = False
            self.TempCoTabModeWidget = QWidget(self.TempCoWidget)
            self.TempCoTabModeWidget.setGeometry(460, 300, 90, 150)
            self.TempCoTabModeLabel = QLabel(self.TempCoTabModeWidget)
            self.TempCoTabModeLabel.setGeometry(0, 0, 90, 150)
            self.TempCoTabModeLabel.setPixmap(QPixmap("Label/TempCoBTNLabel3.png"))
            self.TempCoTabModeLabel1 = QLabel(self.TempCoTabModeWidget)
            self.TempCoTabModeLabel1.setGeometry(20, 19, 50, 50)
            self.TempCoTabModeLabel1.setPixmap(QPixmap("Label/TempCoManualLabelBTN.png"))
            self.TempCoTabModeLabel1.setGraphicsEffect(Shadow(1, 1, 2, 2))
            self.TempCoTabModeBTN = QPushButton(self.TempCoTabModeWidget)
            self.TempCoTabModeBTN.setGeometry(9, 0, 72, 150)
            self.TempCoTabModeBTN.setIcon(QIcon(""))
            self.TempCoTabModeBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.TempCoTabModeBTN.clicked.connect(self.TempCoModeDef)
            self.TempCoTabModeBool = False
        if ("MusicTab" is not None):
            self.MusicTabWidget = QWidget(self)
            self.MusicTabWidget.setGeometry(674, 125, 350, 350)
            self.MusicTabWidgetLabel = QLabel(self.MusicTabWidget)
            self.MusicTabWidgetLabel.setGeometry(0, 0, 350, 350)
            self.MusicTabWidgetLabel.setPixmap(QPixmap("Label/MusicTab.png"))
            self.MusicTabWidgetLabel.setGraphicsEffect(Opacity(0.5))

            self.MusicTabVolumeUp = QPushButton(self.MusicTabWidget)
            self.MusicTabVolumeUp.setGeometry(30, 25, 50, 50)
            self.MusicTabVolumeUp.setIcon(QIcon("Label/Music/VolumeUp.png"))
            self.MusicTabVolumeUp.setIconSize(QSize(50, 50))
            self.MusicTabVolumeUp.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MusicTabVolumeUp.setGraphicsEffect(Opacity(0.4))
            self.MusicTabVolumeUp.clicked.connect(self.MusicTabVolumeUpDef)

            self.MusicTabVolumeDown = QPushButton(self.MusicTabWidget)
            self.MusicTabVolumeDown.setGeometry(110, 25, 50, 50)
            self.MusicTabVolumeDown.setIcon(QIcon("Label/Music/VolumeDown.png"))
            self.MusicTabVolumeDown.setIconSize(QSize(50, 50))
            self.MusicTabVolumeDown.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MusicTabVolumeDown.setGraphicsEffect(Opacity(0.4))
            self.MusicTabVolumeDown.clicked.connect(self.MusicTabVolumeDownDef)

            self.MusicTabMode = QPushButton(self.MusicTabWidget)
            self.MusicTabMode.setGeometry(190, 25, 50, 50)
            self.MusicTabMode.setIcon(QIcon("Label/Music/Normal.png"))
            self.MusicTabMode.setIconSize(QSize(50, 50))
            self.MusicTabMode.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MusicTabMode.setGraphicsEffect(Opacity(0.4))
            self.MusicTabMode.clicked.connect(self.MusicTabModeDef)

            self.MusicTabFolder = QPushButton(self.MusicTabWidget)
            self.MusicTabFolder.setGeometry(270, 25, 50, 50)
            self.MusicTabFolder.setIcon(QIcon("Label/Music/Folder.png"))
            self.MusicTabFolder.setIconSize(QSize(50, 50))
            self.MusicTabFolder.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MusicTabFolder.setGraphicsEffect(Opacity(0.4))
            self.MusicTabFolder.clicked.connect(self.MusicTabFolderDef)

            self.MusicTabBack = QPushButton(self.MusicTabWidget)
            self.MusicTabBack.setGeometry(30, 147, 50, 56)
            self.MusicTabBack.setIcon(QIcon("Label/back.png"))
            self.MusicTabBack.setIconSize(QSize(50, 56))
            self.MusicTabBack.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MusicTabBack.setGraphicsEffect(Opacity(0.4))
            self.MusicTabBack.clicked.connect(self.BackMusicDef)

            self.MusicTabPlay = QPushButton(self.MusicTabWidget)
            self.MusicTabPlay.setGeometry(131, 131, 80, 88)
            self.MusicTabPlay.setIcon(QIcon("Label/play.png"))
            self.MusicTabPlay.setIconSize(QSize(80, 88))
            self.MusicTabPlay.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MusicTabPlay.setGraphicsEffect(Opacity(0.4))
            self.MusicTabPlay.clicked.connect(self.PlayMusicDef)

            self.MusicTabNext = QPushButton(self.MusicTabWidget)
            self.MusicTabNext.setGeometry(270, 147, 50, 56)
            self.MusicTabNext.setIcon(QIcon("Label/next.png"))
            self.MusicTabNext.setIconSize(QSize(50, 56))
            self.MusicTabNext.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.MusicTabNext.setGraphicsEffect(Opacity(0.4))
            self.MusicTabNext.clicked.connect(self.NextMusicDef)

            self.MusicTabNameMusic = QLabel(self.MusicTabWidget)
            self.MusicTabNameMusic.setGeometry(0, 240, 350, 50)
            self.MusicTabNameMusic.setText("Dele Man")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(35)
            self.MusicTabNameMusic.setFont(self.EbrimaFont)
            self.MusicTabNameMusic.setAlignment(Qt.AlignCenter)
            self.MusicTabNameMusic.setStyleSheet('color:white;')
            self.MusicTabNameMusic.setGraphicsEffect(Opacity(0.7))

            self.MusicTabNameArtist = QLabel(self.MusicTabWidget)
            self.MusicTabNameArtist.setGeometry(0, 280, 350, 50)
            self.MusicTabNameArtist.setText("Mohsen Chavoshi")
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(20)
            self.MusicTabNameArtist.setFont(self.EbrimaFont)
            self.MusicTabNameArtist.setAlignment(Qt.AlignCenter)
            self.MusicTabNameArtist.setStyleSheet('color:white;')
            self.MusicTabNameArtist.setGraphicsEffect(Opacity(0.6))
        if ("SocialTab" is not None):
            self.SocialTabWidget = QWidget(self)
            self.SocialTabWidget.setGeometry(274, 50, 750, 300)
            self.SocialTabLabel = QLabel(self.SocialTabWidget)
            self.SocialTabLabel.setGeometry(0, 0, 750, 300)
            self.SocialTabLabel.setPixmap(QPixmap("Label/SocialTab.png"))
            self.SocialTabLabel.setGraphicsEffect(Opacity(0.5))

            self.SocialTabTXT = QLabel(self.SocialTabWidget)
            self.SocialTabTXT.setGeometry(50, 50, 700, 250)
            self.SocialTabTXT.setPixmap(QPixmap("Label/SocialTab.png"))
            self.BaleBot1 = "MAJN : turn off"
            self.BaleBot2 = "Father : Turn on"
            self.BaleBot3 = "MAJN : All off"
            self.BaleBot4 = "Father : Turn off"
            self.BaleBot5 = "MAJN : All on"
            self.SocialTabTXT.setText("<h3>The last five orders:</h3>" + self.BaleBot1
                                      + "<br/>" + self.BaleBot2 + "<br/>" + self.BaleBot3
                                      + "<br/>" + self.BaleBot4 + "<br/>" + self.BaleBot5)
            self.EbrimaFont = QFont()
            self.EbrimaFont.setFamily('Ebrima')
            self.EbrimaFont.setPixelSize(20)
            self.SocialTabTXT.setFont(self.EbrimaFont)
            self.SocialTabTXT.setAlignment(Qt.AlignHCenter)
            self.SocialTabTXT.setStyleSheet('color:black;')
            self.SocialTabTXT.setGraphicsEffect(Opacity(0.6))

            self.SocialTabBTN = QPushButton(self.SocialTabWidget)
            self.SocialTabBTN.setGeometry(0, 0, 750, 300)
            self.SocialTabBTN.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.SocialTabBTN.setGraphicsEffect(Opacity(0.8))
        if ("SettingTab" is not None):
            self.SettingWidget = QWidget(self)
            self.SettingWidget.setGeometry(274, 75, 750, 500)
            self.SettingTabWidget1 = QWidget(self.SettingWidget)
            self.SettingTabWidget1.setGeometry(0, 0, 750, 200)
            self.SettingTabLabel1 = QLabel(self.SettingTabWidget1)
            self.SettingTabLabel1.setGeometry(0, 0, 750, 200)
            self.SettingTabLabel1.setPixmap(QPixmap("Label/Setting/Label1.png"))
            self.SettingTabLabel1.setGraphicsEffect(Opacity(0.8))

            self.SettingTabAI = QPushButton(self.SettingTabWidget1)
            self.SettingTabAI.setGeometry(100, 50, 100, 100)
            self.SettingTabAI.setIcon(QIcon("Label/Setting/AIOFF.png"))
            self.SettingTabAI.setIconSize(QSize(100, 100))
            self.SettingTabAI.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.SettingTabAI.setGraphicsEffect(Opacity(0.4))
            self.SettingTabAI.clicked.connect(self.SettingTabAIDef)
            self.SettingTabAIB = False

            self.SettingTabTheme = QPushButton(self.SettingTabWidget1)
            self.SettingTabTheme.setGeometry(325, 50, 100, 100)
            self.SettingTabTheme.setIcon(QIcon("Label/Setting/Theme.png"))
            self.SettingTabTheme.setIconSize(QSize(100, 100))
            self.SettingTabTheme.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.SettingTabTheme.setGraphicsEffect(Opacity(0.4))
            self.SettingTabTheme.clicked.connect(self.BGPathDef)

            self.SettingTabSaveCam = QPushButton(self.SettingTabWidget1)
            self.SettingTabSaveCam.setGeometry(550, 50, 100, 100)
            self.SettingTabSaveCam.setIcon(QIcon("Label/Setting/SaveCam.png"))
            self.SettingTabSaveCam.setIconSize(QSize(100, 100))
            self.SettingTabSaveCam.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.SettingTabSaveCam.setGraphicsEffect(Opacity(0.4))
            self.SettingTabSaveCam.clicked.connect(self.SettingTabSaveCamDef)
            self.SettingTabSaveCamPath = ""

            self.SettingTabWidget2 = QWidget(self.SettingWidget)
            self.SettingTabWidget2.setGeometry(0, 250, 750, 200)
            self.SettingTabLabel2 = QLabel(self.SettingTabWidget2)
            self.SettingTabLabel2.setGeometry(0, 0, 750, 200)
            self.SettingTabLabel2.setPixmap(QPixmap("Label/Setting/Label1.png"))
            self.SettingTabLabel2.setGraphicsEffect(Opacity(0.8))

            self.SettingTabClockLabel = QLabel(self.SettingTabWidget2)
            self.SettingTabClockLabel.setGeometry(45, 60, 280, 80)
            self.SettingTabClockLabel.setPixmap(QPixmap("Label/Setting/ClockLabel.png"))
            self.SettingTabClockLabel.setGraphicsEffect(Opacity(0.4))
            if ("H" != None):
                Time = "06:35:35"
                self.SettingTabH = QLabel(self.SettingTabWidget2)
                self.SettingTabH.setGeometry(45, 57, 80, 80)
                self.SettingTabH.setText(Time[:2])
                self.EbrimaFont = QFont()
                self.EbrimaFont.setFamily('Ebrima')
                self.EbrimaFont.setPixelSize(60)
                self.SettingTabH.setFont(self.EbrimaFont)
                self.SettingTabH.setAlignment(Qt.AlignCenter)
                self.SettingTabH.setStyleSheet('color:black;')
                self.SettingTabH.setGraphicsEffect(Opacity(0.7))

                self.SettingTabHUp = QPushButton(self.SettingTabWidget2)
                self.SettingTabHUp.setGeometry(55, 15, 60, 60)
                self.SettingTabHUp.setIcon(QIcon("Label/Setting/Up.png"))
                self.SettingTabHUp.setIconSize(QSize(60, 60))
                self.SettingTabHUp.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabHUp.setGraphicsEffect(Opacity(0.2))
                self.SettingTabHUp.pressed.connect(self.SettingTabHUpDef)

                self.SettingTabHDown = QPushButton(self.SettingTabWidget2)
                self.SettingTabHDown.setGeometry(55, 125, 60, 60)
                self.SettingTabHDown.setIcon(QIcon("Label/Setting/Down.png"))
                self.SettingTabHDown.setIconSize(QSize(60, 60))
                self.SettingTabHDown.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabHDown.setGraphicsEffect(Opacity(0.2))
                self.SettingTabHDown.pressed.connect(self.SettingTabHDownDef)
            if ("M" != None):
                self.SettingTabM = QLabel(self.SettingTabWidget2)
                self.SettingTabM.setGeometry(145, 57, 80, 80)
                self.SettingTabM.setText(Time[3:5])
                self.EbrimaFont = QFont()
                self.EbrimaFont.setFamily('Ebrima')
                self.EbrimaFont.setPixelSize(60)
                self.SettingTabM.setFont(self.EbrimaFont)
                self.SettingTabM.setAlignment(Qt.AlignCenter)
                self.SettingTabM.setStyleSheet('color:black;')
                self.SettingTabM.setGraphicsEffect(Opacity(0.7))

                self.SettingTabMUp = QPushButton(self.SettingTabWidget2)
                self.SettingTabMUp.setGeometry(155, 15, 60, 60)
                self.SettingTabMUp.setIcon(QIcon("Label/Setting/Up.png"))
                self.SettingTabMUp.setIconSize(QSize(60, 60))
                self.SettingTabMUp.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabMUp.setGraphicsEffect(Opacity(0.2))
                self.SettingTabMUp.pressed.connect(self.SettingTabMUpDef)

                self.SettingTabMDown = QPushButton(self.SettingTabWidget2)
                self.SettingTabMDown.setGeometry(155, 125, 60, 60)
                self.SettingTabMDown.setIcon(QIcon("Label/Setting/Down.png"))
                self.SettingTabMDown.setIconSize(QSize(60, 60))
                self.SettingTabMDown.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabMDown.setGraphicsEffect(Opacity(0.2))
                self.SettingTabMDown.pressed.connect(self.SettingTabMDownDef)
            if ("S" != None):
                self.SettingTabS = QLabel(self.SettingTabWidget2)
                self.SettingTabS.setGeometry(245, 57, 80, 80)
                self.SettingTabS.setText(Time[6:8])
                self.EbrimaFont = QFont()
                self.EbrimaFont.setFamily('Ebrima')
                self.EbrimaFont.setPixelSize(60)
                self.SettingTabS.setFont(self.EbrimaFont)
                self.SettingTabS.setAlignment(Qt.AlignCenter)
                self.SettingTabS.setStyleSheet('color:black;')
                self.SettingTabS.setGraphicsEffect(Opacity(0.7))

                self.SettingTabSUp = QPushButton(self.SettingTabWidget2)
                self.SettingTabSUp.setGeometry(255, 15, 60, 60)
                self.SettingTabSUp.setIcon(QIcon("Label/Setting/Up.png"))
                self.SettingTabSUp.setIconSize(QSize(60, 60))
                self.SettingTabSUp.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabSUp.setGraphicsEffect(Opacity(0.2))
                self.SettingTabSUp.pressed.connect(self.SettingTabSUpDef)

                self.SettingTabSDown = QPushButton(self.SettingTabWidget2)
                self.SettingTabSDown.setGeometry(255, 125, 60, 60)
                self.SettingTabSDown.setIcon(QIcon("Label/Setting/Down.png"))
                self.SettingTabSDown.setIconSize(QSize(60, 60))
                self.SettingTabSDown.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabSDown.setGraphicsEffect(Opacity(0.2))
                self.SettingTabSDown.pressed.connect(self.SettingTabSDownDef)
            if ("Week" != None):
                self.SettingTabSaturday = QPushButton(self.SettingTabWidget2)
                self.SettingTabSaturday.setGeometry(350, 15, 50, 50)
                self.SettingTabSaturday.setIcon(QIcon("Label/Setting/SON.png"))
                self.SettingTabSaturday.setIconSize(QSize(50, 50))
                self.SettingTabSaturday.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabSaturday.setGraphicsEffect(Opacity(0.4))
                self.SettingTabSaturday.clicked.connect(self.SettingTabSaturdayDef)
                self.SettingTabSaturdayB = True
                self.SettingTabSunday = QPushButton(self.SettingTabWidget2)
                self.SettingTabSunday.setGeometry(410, 15, 50, 50)
                self.SettingTabSunday.setIcon(QIcon("Label/Setting/SON.png"))
                self.SettingTabSunday.setIconSize(QSize(50, 50))
                self.SettingTabSunday.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabSunday.setGraphicsEffect(Opacity(0.4))
                self.SettingTabSunday.clicked.connect(self.SettingTabSundayDef)
                self.SettingTabSundayB = True
                self.SettingTabMonday = QPushButton(self.SettingTabWidget2)
                self.SettingTabMonday.setGeometry(350, 75, 50, 50)
                self.SettingTabMonday.setIcon(QIcon("Label/Setting/MON.png"))
                self.SettingTabMonday.setIconSize(QSize(50, 50))
                self.SettingTabMonday.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabMonday.setGraphicsEffect(Opacity(0.4))
                self.SettingTabMonday.clicked.connect(self.SettingTabMondayDef)
                self.SettingTabMondayB = True
                self.SettingTabTuesday = QPushButton(self.SettingTabWidget2)
                self.SettingTabTuesday.setGeometry(410, 75, 50, 50)
                self.SettingTabTuesday.setIcon(QIcon("Label/Setting/TON.png"))
                self.SettingTabTuesday.setIconSize(QSize(50, 50))
                self.SettingTabTuesday.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabTuesday.setGraphicsEffect(Opacity(0.4))
                self.SettingTabTuesday.clicked.connect(self.SettingTabTuesdayDef)
                self.SettingTabTuesdayB = True
                self.SettingTabWednesday = QPushButton(self.SettingTabWidget2)
                self.SettingTabWednesday.setGeometry(350, 135, 50, 50)
                self.SettingTabWednesday.setIcon(QIcon("Label/Setting/WON.png"))
                self.SettingTabWednesday.setIconSize(QSize(50, 50))
                self.SettingTabWednesday.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabWednesday.setGraphicsEffect(Opacity(0.4))
                self.SettingTabWednesday.clicked.connect(self.SettingTabWednesdayDef)
                self.SettingTabWednesdayB = True
                self.SettingTabThursday = QPushButton(self.SettingTabWidget2)
                self.SettingTabThursday.setGeometry(410, 135, 50, 50)
                self.SettingTabThursday.setIcon(QIcon("Label/Setting/TON.png"))
                self.SettingTabThursday.setIconSize(QSize(50, 50))
                self.SettingTabThursday.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabThursday.setGraphicsEffect(Opacity(0.4))
                self.SettingTabThursday.clicked.connect(self.SettingTabThursdayDef)
                self.SettingTabThursdayB = True
                self.SettingTabFriday = QPushButton(self.SettingTabWidget2)
                self.SettingTabFriday.setGeometry(470, 75, 50, 50)
                self.SettingTabFriday.setIcon(QIcon("Label/Setting/FOFF.png"))
                self.SettingTabFriday.setIconSize(QSize(50, 50))
                self.SettingTabFriday.setStyleSheet("border-radius: 5%;outline-style: initial;")
                self.SettingTabFriday.setGraphicsEffect(Opacity(0.4))
                self.SettingTabFriday.clicked.connect(self.SettingTabFridayDef)
                self.SettingTabFridayB = False
            self.SettingTabWidget3 = QWidget(self.SettingWidget)
            self.SettingTabWidget3.setGeometry(550, 250, 200, 200)
            self.SettingTabLabel3 = QLabel(self.SettingTabWidget3)
            self.SettingTabLabel3.setGeometry(0, 0, 200, 200)
            self.SettingTabLabel3.setPixmap(QPixmap("Label/Setting/Label2.png"))
            self.SettingTabLabel3.setGraphicsEffect(Opacity(0.8))

            self.SettingTabAlarm = QPushButton(self.SettingTabWidget3)
            self.SettingTabAlarm.setGeometry(50, 50, 100, 100)
            self.SettingTabAlarm.setIcon(QIcon("Label/Setting/AlarmON.png"))
            self.SettingTabAlarm.setIconSize(QSize(100, 100))
            self.SettingTabAlarm.setStyleSheet("border-radius: 5%;outline-style: initial;")
            self.SettingTabAlarm.setGraphicsEffect(Opacity(0.4))
            self.SettingTabAlarm.clicked.connect(self.SettingTabAlarmDef)
            self.SettingTabAlarmB = True
            self.SettingTabAlarmAnim = QPropertyAnimation(self.SettingTabWidget2, 'geometry')
        if ("UI Anim" is not None):
            self.HomeBTN = QPushButton(self)
            self.HomeBTN.setGeometry(0, 0, 0, 0)
            self.RoomBTN = QPushButton(self)
            self.RoomBTN.setGeometry(0, 0, 0, 0)
            self.TempCoBTN = QPushButton(self)
            self.TempCoBTN.setGeometry(0, 0, 0, 0)
            self.MusicBTN = QPushButton(self)
            self.MusicBTN.setGeometry(0, 0, 0, 0)
            self.SocialBTN = QPushButton(self)
            self.SocialBTN.setGeometry(0, 0, 0, 0)
            self.SettingBTN = QPushButton(self)
            self.SettingBTN.setGeometry(0, 0, 0, 0)

            self.machine = QStateMachine()
            self.HomeState = QState(self.machine)
            self.RoomState = QState(self.machine)
            self.TempCoState = QState(self.machine)
            self.MusicState = QState(self.machine)
            self.SocialState = QState(self.machine)
            self.SettingState = QState(self.machine)
            self.machine.setInitialState(self.HomeState)

            self.HomeState.assignProperty(self.HomeTabWidget, 'pos', QPointF(774, 50))
            self.HomeState.assignProperty(self.RoomTabWidget, 'pos', QPointF(1024, 50))
            self.HomeState.assignProperty(self.TempCoWidget, 'pos', QPointF(1024, 50))
            self.HomeState.assignProperty(self.MusicTabWidget, 'pos', QPointF(1024, 125))
            self.HomeState.assignProperty(self.SocialTabWidget, 'pos', QPointF(1024, 50))
            self.HomeState.assignProperty(self.SettingWidget, 'pos', QPointF(1024, 75))

            self.RoomState.assignProperty(self.HomeTabWidget, 'pos', QPointF(1024, 50))
            self.RoomState.assignProperty(self.RoomTabWidget, 'pos', QPointF(274, 50))
            self.RoomState.assignProperty(self.TempCoWidget, 'pos', QPointF(1024, 50))
            self.RoomState.assignProperty(self.MusicTabWidget, 'pos', QPointF(1024, 125))
            self.RoomState.assignProperty(self.SocialTabWidget, 'pos', QPointF(1024, 50))
            self.RoomState.assignProperty(self.SettingWidget, 'pos', QPointF(1024, 75))

            self.TempCoState.assignProperty(self.HomeTabWidget, 'pos', QPointF(1024, 50))
            self.TempCoState.assignProperty(self.RoomTabWidget, 'pos', QPointF(1024, 50))
            self.TempCoState.assignProperty(self.TempCoWidget, 'pos', QPointF(474, 50))
            self.TempCoState.assignProperty(self.MusicTabWidget, 'pos', QPointF(1024, 125))
            self.TempCoState.assignProperty(self.SocialTabWidget, 'pos', QPointF(1024, 50))
            self.TempCoState.assignProperty(self.SettingWidget, 'pos', QPointF(1024, 75))

            self.MusicState.assignProperty(self.HomeTabWidget, 'pos', QPointF(1024, 50))
            self.MusicState.assignProperty(self.RoomTabWidget, 'pos', QPointF(1024, 50))
            self.MusicState.assignProperty(self.TempCoWidget, 'pos', QPointF(1024, 50))
            self.MusicState.assignProperty(self.MusicTabWidget, 'pos', QPointF(674, 125))
            self.MusicState.assignProperty(self.SocialTabWidget, 'pos', QPointF(1024, 50))
            self.MusicState.assignProperty(self.SettingWidget, 'pos', QPointF(1024, 75))

            self.SocialState.assignProperty(self.HomeTabWidget, 'pos', QPointF(1024, 50))
            self.SocialState.assignProperty(self.RoomTabWidget, 'pos', QPointF(1024, 50))
            self.SocialState.assignProperty(self.TempCoWidget, 'pos', QPointF(1024, 50))
            self.SocialState.assignProperty(self.MusicTabWidget, 'pos', QPointF(1024, 125))
            self.SocialState.assignProperty(self.SocialTabWidget, 'pos', QPointF(274, 50))
            self.SocialState.assignProperty(self.SettingWidget, 'pos', QPointF(1024, 75))

            self.SettingState.assignProperty(self.HomeTabWidget, 'pos', QPointF(1024, 50))
            self.SettingState.assignProperty(self.RoomTabWidget, 'pos', QPointF(1024, 50))
            self.SettingState.assignProperty(self.TempCoWidget, 'pos', QPointF(1024, 50))
            self.SettingState.assignProperty(self.MusicTabWidget, 'pos', QPointF(1024, 125))
            self.SettingState.assignProperty(self.SocialTabWidget, 'pos', QPointF(1024, 50))
            self.SettingState.assignProperty(self.SettingWidget, 'pos', QPointF(274, 75))

            self.machine.start()
            self.HomeBTN.clicked.connect(self.HomeDefAnim)
            self.RoomBTN.clicked.connect(self.RoomDefAnim)
            self.TempCoBTN.clicked.connect(self.TempCoDefAnim)
            self.MusicBTN.clicked.connect(self.MusicDefAnim)
            self.SocialBTN.clicked.connect(self.SocialDefAnim)
            self.SettingBTN.clicked.connect(self.SettingDefAnim)
            self.RoomTabBTN1ON.clicked.connect(self.RoomTabBTN1Def)
            self.RoomTabBTN1Bool = False
            self.RoomTabBTN2ON.clicked.connect(self.RoomTabBTN2Def)
            self.RoomTabBTN2Bool = False
            self.RoomTabBTN3ON.clicked.connect(self.RoomTabBTN3Def)
            self.RoomTabBTN3Bool = False
            self.RoomTabBTN4ON.clicked.connect(self.RoomTabBTN4Def)
            self.RoomTabBTN4Bool = False
            self.HomeState = "Home"
            self.FadeUnfadeAnim = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.FadeUpFadeDownAnim = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.ChangeImageFade = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.ChangeImageFade1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.ChangeImageFadeGroup = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.FadeIO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.FadeTimerHome = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.AnimG1 = QSequentialAnimationGroup()

            self.AnimG2 = QParallelAnimationGroup()

            self.AnimG3 = QParallelAnimationGroup()

            self.AnimG4 = QParallelAnimationGroup()
        if ("Clocks" is not None):
            self.ClockHome = QTimer(self)
            self.ClockHome.setInterval(1000)
            self.ClockHome.timeout.connect(self.ClockHomeDef)
            self.ClockHome.start()

            self.RoomTabBTNsTimer = QTimer(self)
            self.RoomTabBTNsTimer.setInterval(2000)
            self.RoomTabBTNsTimer.timeout.connect(self.RoomTabBTNsDef)
            self.RoomTabBTNsTimer.start()

            self.BGTimer = QTimer(self)
            self.BGTimer.setInterval(1000)
            self.BGTimer.timeout.connect(self.BGTimerDef)
            self.BGTimer.start()

            self.MusicDef = QTimer(self)
            self.MusicDef.setInterval(1000)
            self.MusicDef.timeout.connect(self.MusicTimerDef)
            self.MusicDef.start()

            self.AlarmTimer = QTimer(self)
            self.AlarmTimer.setInterval(1000)
            self.AlarmTimer.timeout.connect(self.AlarmDef)
            self.AlarmTimer.start()

            self.security = QTimer(self)
            self.security.setInterval(500)
            self.securityBool = False
            self.bot = bot
            self.security.timeout.connect(self.SecurityDef)
            self.security.start()
            self.securityCount = 0

            # ! self.AITimer = QTimer(self)
            # ! self.AITimer.setInterval(1000)
            # ! self.AITimer.timeout.connect(self.AIDef)
            # ! self.AITimer.start()
        if ("Azan" is not None):
            self.timeir = str(urllib3.PoolManager().request('GET', 'http://www.time.ir/').data)
            self.AzanMorningInt = self.timeir.find("lblAzanMorning\" class=\"inlineBlock ltr text-nowrap\">") + len(
                "lblAzanMorning\" class=\"inlineBlock ltr text-nowrap\">")
            self.AzanMorning = self.timeir[self.AzanMorningInt:self.AzanMorningInt + 31]
            self.AzanMorning = self.AzanMorning.replace("&#1776;", "0", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1777;", "1", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1778;", "2", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1779;", "3", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1780;", "4", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1781;", "5", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1782;", "6", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1783;", "7", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1784;", "8", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1785;", "9", 4)
            self.AzanMorning = self.AzanMorning.replace(" ", "", 4)
            self.AzanNoonInt = self.timeir.find("lblAzanNoon\" class=\"inlineBlock ltr text-nowrap\">") + len(
                "lblAzanNoon\" class=\"inlineBlock ltr text-nowrap\">")
            self.AzanNoon = self.timeir[self.AzanNoonInt:self.AzanNoonInt + 31]
            self.AzanNoon = self.AzanNoon.replace("&#1776;", "0", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1777;", "1", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1778;", "2", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1779;", "3", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1780;", "4", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1781;", "5", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1782;", "6", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1783;", "7", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1784;", "8", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1785;", "9", 4)
            self.AzanNoon = self.AzanNoon.replace(" ", "", 4)
            self.AzanNightInt = self.timeir.find("lblAzanNight\" class=\"inlineBlock ltr text-nowrap\">") + len(
                "lblAzanNight\" class=\"inlineBlock ltr text-nowrap\">")
            self.AzanNight = self.timeir[self.AzanNightInt:self.AzanNightInt + 31]
            self.AzanNight = self.AzanNight.replace("&#1776;", "0", 4)
            self.AzanNight = self.AzanNight.replace("&#1777;", "1", 4)
            self.AzanNight = self.AzanNight.replace("&#1778;", "2", 4)
            self.AzanNight = self.AzanNight.replace("&#1779;", "3", 4)
            self.AzanNight = self.AzanNight.replace("&#1780;", "4", 4)
            self.AzanNight = self.AzanNight.replace("&#1781;", "5", 4)
            self.AzanNight = self.AzanNight.replace("&#1782;", "6", 4)
            self.AzanNight = self.AzanNight.replace("&#1783;", "7", 4)
            self.AzanNight = self.AzanNight.replace("&#1784;", "8", 4)
            self.AzanNight = self.AzanNight.replace("&#1785;", "9", 4)
            self.AzanNight = self.AzanNight.replace(" ", "", 4)
            print(self.AzanMorning)
            print(self.AzanNoon)
            print(self.AzanNight)
        if ("Temp" is not None):
            hm, tm = 35, 35  # ! Adafruit_DHT.read_retry(22, 4)
            self.TempCheckAve = tm
            self.HumiCheckAve = hm
            self.HomeTabTempText.setText(str(int(self.TempCheckAve)))
            self.HomeTabHumidityText.setText(str(int(hm)))
            self.TempCoTabAutoOutsideTempTXT.setText(str(int(self.TempCheckAve)))
        if ("BaleBot" is not None):
            global home_markup
            bot.sendMessage(chat_id=MAJN_ID, text='I\'ve restarted \nHome:', reply_markup=home_markup)
            #bot.sendMessage(chat_id=Father_ID, text='I\'ve restarted \nHome:', reply_markup=markup)
            #bot.sendMessage(chat_id=Mother_ID, text='I\'ve restarted \nHome:', reply_markup=markup)
            #self.BaleBotT = newThread(self.BaleBotDef)
            self.BaleBotT = QTimer(self)
            self.BaleBotT.timeout.connect(self.BaleBotDef)
            self.BaleBotT.setInterval(200)
            self.BaleBotT.start()
            self.BotDelayControl = 0
            self.Clicked = False
            self.LastOrderName = "MAJN"
            self.LastSongName = self.MusicTabNameMusic.text()
        if ("msgBox"):
            self.msgBox = QMessageBox(self)
            self.msgBox.setWindowTitle("Msg")
            self.msgBox.setIcon(QMessageBox.Warning)
            resolution = QDesktopWidget().screenGeometry()
            self.msgBox.move((resolution.width() / 2) - (self.frameSize().width() / 2) - 100,
                             (resolution.height() / 2) - (self.frameSize().height() / 2))
            self.msgBox.setStyleSheet("color: blue;")
            self.hide()

    def BaleBotDef(self):
        global update_id
        global home_markup
        global room_markup
        global setting_markup
        try:
            for update in bot.get_updates(offset=update_id):
                update_id = update.update_id + 1
                if update.message:
                    command = update.message.text
                    chat_id = update.effective_chat.id
                    if(update.effective_chat.id == MAJN_ID):
                        self.LastOrderName = "MAJN"
                    elif(update.effective_chat.id == Father_ID):
                        self.LastOrderName = "Father"
                    elif(update.effective_chat.id == Mother_ID):
                        self.LastOrderName = "Mother"
                    elif(update.effective_chat.id == Alirezaishisname):
                        self.LastOrderName = "AlirezaH"
                    if (update.effective_chat.id != MAJN_ID and update.effective_chat.id != Father_ID and update.effective_chat.id != Mother_ID and update.effective_chat.id != Alirezaishisname):
                        text = "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\nSomeone used 3MAJN5 bot\n"
                        try:
                            text += "Name : " + str(update.message.from_user.first_name) + " " + str(
                                update.message.from_user.lastname) + "\n"
                        except:
                            x = 0
                        try:
                            text += "Username : @" + str(update.message.from_user.username) + "\n"
                        except:
                            x = 0
                        text += "Chat ID : " + str(update.effective_chat.id) + "\n"
                        text += "Text : " + str(update.message.text) + "\n"
                        bot.send_message(chat_id=MAJN_ID, text=text)
                        bot.sendMessage(chat_id=update.effective_chat.id, text=
                        'Access denied!!!\n❌⛔🚫❌⛔🚫\n'
                        '✋You can\'t use this bot\nYour data sent to MAJN...')
                    elif (command == '/start'):
                        bot.sendMessage(chat_id=chat_id, text='Home:', reply_markup=home_markup)
                    elif (command == '🏠 Home 🏠'):
                        bot.sendMessage(chat_id=chat_id, text='Home:', reply_markup=home_markup)
                    elif (command == '📊 Info 📊'):
                        info = "        📊 Info 📊\nHello :)"
                        info += "\n"
                        try:
                            info += update.message.from_user.first_name + " "
                        except:
                            x=0
                        try:
                            info += update.message.from_user.lastname + " "
                        except:
                            x=0
                        info += "\n"
                        info += self.HomeTabDate.text() + "\n"
                        info += self.HomeTabDay.text() + "\n"
                        info += "\n🌦️" + self.HomeTabWeatherLabel.text() + "🌦️\n"
                        info += "\n🕞" + self.HomeTabClockH.text() + ":" + self.HomeTabClockM.text() + ":" + self.HomeTabClockS.text() + "🕞\n"
                        info += "⏰" + self.SettingTabH.text() + ":" + self.SettingTabM.text() + ":" + self.SettingTabS.text() + "⏰\n"
                        info += "\n⏰ : " + str(self.SettingTabAlarmB)
                        info += "\nInside : \n" + "🌡 : " + str(self.TempCheckAve)[:4] +"\n"
                        info += "C 💧 : " + str(self.HumiCheckAve)[:4] + "%\n"
                        info += "Outside : \n" + "🌡 : " + str(self.OutsideTempW)[:4] +"\n"
                        info += "C 💧 : " + str(self.OutSideHumidityW)[:4] + "%\n"
                        info += "\n🎵 : " + self.MusicTabNameMusic.text() + "\n"
                        info += "🎤 : " + self.MusicTabNameArtist.text() + "\n\n"
                        info += "🔒 Security : " + str(self.securityBool) + "\n"
                        # ! info += "👀Is anyone in room : " + str(bool(GPIO.input(16))) + "\n"
                        info += "🤖AI : " + str(self.SettingTabAIB) + "\n"
                        info += "\n🕋Sobh :       " + self.AzanMorning + " " + str(self.AzanSobh) + "\n"
                        info += "🕋Zohr :        " + self.AzanNoon + " " + str(self.AzanZohr) + "\n"
                        info += "🕋Magherb : " + self.AzanNight + " " + str(self.AzanMaghreb) + "\n"
                        bot.sendMessage(chat_id, info.ljust(20))
                    elif (command == '⏮'):
                        self.HomeTabMusicBack.click()
                        bot.sendMessage(chat_id,'⏮')
                        newOrder(self,'Back Music')
                    elif (command == '⏯'):
                        self.HomeTabMusicPlay.click()
                        bot.sendMessage(chat_id=chat_id, text="Playing music is :" + str(not self.MusicPlaying))
                        newOrder(self,'Play/Pause Music')
                        bot.sendMessage(chat_id=chat_id, text="Song :" + str(self.MusicTabNameMusic.text()) + "\nArtist :" + str(
                            self.MusicTabNameArtist.text()))
                    elif (command == '⏭'):
                        self.HomeTabMusicNext.click()
                        bot.sendMessage(chat_id,'⏭')
                        newOrder(self,'Next Music')
                    elif (command == '🔇'):
                        self.SetVolume(0)
                        self.Volume = 0
                        newOrder(self,'Mute')
                        bot.sendMessage(chat_id, 'Muted')
                        self.ChangeImageFading(self.MusicTabVolume, 10, 0.4, "Label/Music/Mute.png")
                    elif (command == '🔊'):
                        self.Volume = self.Volume + 0.5
                        self.SetVolume(self.Volume)
                        newOrder(self,'More Volume')
                        bot.sendMessage(chat_id, 'Volume has been increased...')
                        self.ChangeImageFading(self.MusicTabVolume, 7, 0.4, "Label/Music/High.png")
                    elif (command == '🎛️ Room 🎛️'):
                        if (chat_id == MAJN_ID):
                            bot.sendMessage(chat_id, 'Control your room Mohammadali:', reply_markup=room_markup)
                        if (chat_id == Father_ID):
                            bot.sendMessage(chat_id, 'Control your home Alireza:', reply_markup=room_markup)
                        if (chat_id == Alirezaishisname):
                            bot.sendMessage(chat_id, 'Control Hydronable:', reply_markup=room_markup)
                        if (chat_id == Mother_ID):
                            bot.sendMessage(chat_id, 'Control your home Saedeh:', reply_markup=room_markup)
                    elif (command == '💡'):
                        self.RoomTabBTN1ON.click()
                        newOrder(self,'Lamp' + " : " + str(self.RoomTabBTN1Bool))
                        if(self.SettingTabAIB):
                            self.SettingTabAI.click()
                        bot.sendMessage(chat_id, "💡 turned " + str(self.RoomTabBTN1Bool) + " 💡")
                    elif (command == '🎧'):
                        self.RoomTabBTN4ON.click()
                        newOrder(self,'Speakers' + " : " + str(self.RoomTabBTN4Bool))
                        bot.sendMessage(chat_id, "🎧 turned " + str(self.RoomTabBTN4Bool) + " 🎧")
                    elif (command == '🔌'):
                        self.RoomTabBTN3ON.click()
                        newOrder(self,'Heater' + " : " + str( self.RoomTabBTN3Bool))
                        bot.sendMessage(chat_id, "🔌 turned " + str( self.RoomTabBTN3Bool) + " 🔌")
                    elif (command == '🕯️'):
                        self.RoomTabBTN2ON.click()
                        newOrder(self,'LED' + " : " + str( self.RoomTabBTN2Bool))
                        bot.sendMessage(chat_id, "🕯️ turned " + str( self.RoomTabBTN2Bool) + " 🕯️")
                    elif (command == '🔒️'):
                        self.securityBool = not self.securityBool
                        bot.sendMessage(chat_id, '🔒 is : ' + str(self.securityBool))
                        newOrder(self,'Room Lock' + " : " + str( self.securityBool))
                        if (self.securityBool == True):
                            pygame.init()
                        pygame.mixer.music.load("Images/sounds/_car_lock_.mp3")
                        pygame.mixer.music.play()
                    elif (command == '🤖'):
                        self.SettingTabAI.click()
                        newOrder(self, 'AI' + " : " + str( self.SettingTabAIB))
                        bot.sendMessage(chat_id, '🤖 is : ' + str( self.SettingTabAIB))
                    elif (command == '⚙ Setting ⚙'):
                        bot.sendMessage(chat_id, 'Setting :', reply_markup=setting_markup)
                    elif (command == '📸' or command == 'Take a photo'):
                        # ! camera = PiCamera()
                        # ! time.sleep(2)
                        # ! camera.capture("img.png")
                        # ! del camera
                        bot.sendMessage(MAJN_ID, 'Photo has taken, Sending...')
                        try:
                            bot.send_photo(MAJN_ID, photo=open('img.png', 'rb'))
                        except:
                            pass
                        bot.sendMessage(MAJN_ID, 'Done')
                    elif (command == '⏰ Alarm ⏰'):
                        self.SettingTabAlarm.click()
                        bot.sendMessage(chat_id, '⏰ Alarm ⏰ is : ' + str(not self.SettingTabAlarmB))
                    elif (command == '🕋 Sobh 🕋️'):
                        self.AzanSobh = not self.AzanSobh
                        bot.sendMessage(chat_id, '🕋 Sobh 🕋️ is : ' + str(self.AzanSobh))
                    elif (command == '🕋 Zohr 🕋️'):
                        self.AzanZohr = not self.AzanZohr
                        bot.sendMessage(chat_id, '🕋 Zohr 🕋 is : ' + str(self.AzanZohr))
                    elif (command == '🕋 Maghreb 🕋'):
                        self.AzanMaghreb = not self.AzanMaghreb
                        bot.sendMessage(chat_id, '🕋 Maghreb 🕋 is : ' + str(self.AzanMaghreb))
                    else:
                        bot.sendMessage(chat_id, 'Wrong Command!!!')
                        bot.sendMessage(chat_id, 'Home:', reply_markup=home_markup)
                    break
                break
        except NetworkError:
            x=0
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

    def MenuHomeBTNDef(self):
        self.HomeBTN.click()
        self.HomeState = "Home"
        self.FadeUpFadeDown(self.MenuHomeBTN, 17, 0.7, 0.15)

    def AIDef(self):
        now = datetime.now()
        if (now.minute == 35 and now.second == 35 and now.hour >= 7):
            bot.sendMessage(MAJN_ID, '❤ 35 ❤')
        if (now.minute == 0 and now.second == 35 and now.hour == 0):
            self.randh = randrange(0, 23)
        if (now.hour == 7 and now.minute == 35 and now.second == 5):
            self.timeir = str(urllib3.PoolManager().request('GET', 'http://www.time.ir/').data)
            self.AzanMorningInt = self.timeir.find("lblAzanMorning\" class=\"inlineBlock ltr text-nowrap\">") + len(
                "lblAzanMorning\" class=\"inlineBlock ltr text-nowrap\">")
            self.AzanMorning = self.timeir[self.AzanMorningInt:self.AzanMorningInt + 31]
            self.AzanMorning = self.AzanMorning.replace("&#1776;", "0", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1777;", "1", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1778;", "2", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1779;", "3", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1780;", "4", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1781;", "5", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1782;", "6", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1783;", "7", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1784;", "8", 4)
            self.AzanMorning = self.AzanMorning.replace("&#1785;", "9", 4)
            self.AzanMorning = self.AzanMorning.replace(" ", "", 4)
            self.AzanNoonInt = self.timeir.find("lblAzanNoon\" class=\"inlineBlock ltr text-nowrap\">") + len(
                "lblAzanNoon\" class=\"inlineBlock ltr text-nowrap\">")
            self.AzanNoon = self.timeir[self.AzanNoonInt:self.AzanNoonInt + 31]
            self.AzanNoon = self.AzanNoon.replace("&#1776;", "0", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1777;", "1", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1778;", "2", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1779;", "3", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1780;", "4", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1781;", "5", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1782;", "6", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1783;", "7", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1784;", "8", 4)
            self.AzanNoon = self.AzanNoon.replace("&#1785;", "9", 4)
            self.AzanNoon = self.AzanNoon.replace(" ", "", 4)
            self.AzanNightInt = self.timeir.find("lblAzanNight\" class=\"inlineBlock ltr text-nowrap\">") + len(
                "lblAzanNight\" class=\"inlineBlock ltr text-nowrap\">")
            self.AzanNight = self.timeir[self.AzanNightInt:self.AzanNightInt + 31]
            self.AzanNight = self.AzanNight.replace("&#1776;", "0", 4)
            self.AzanNight = self.AzanNight.replace("&#1777;", "1", 4)
            self.AzanNight = self.AzanNight.replace("&#1778;", "2", 4)
            self.AzanNight = self.AzanNight.replace("&#1779;", "3", 4)
            self.AzanNight = self.AzanNight.replace("&#1780;", "4", 4)
            self.AzanNight = self.AzanNight.replace("&#1781;", "5", 4)
            self.AzanNight = self.AzanNight.replace("&#1782;", "6", 4)
            self.AzanNight = self.AzanNight.replace("&#1783;", "7", 4)
            self.AzanNight = self.AzanNight.replace("&#1784;", "8", 4)
            self.AzanNight = self.AzanNight.replace("&#1785;", "9", 4)
            self.AzanNight = self.AzanNight.replace(" ", "", 4)
            info = "Hello \nGood morning :) \n❤️MAJN❤️"
            info += self.HomeTabDate.text() + "\n"
            info += self.HomeTabDay.text() + "\n"
            info += "\n🌦️" + self.HomeTabWeatherLabel.text() + "🌦️\n"
            info += "\n🕞" + self.HomeTabClockH.text() + ":" + self.HomeTabClockM.text() + ":" + self.HomeTabClockS.text() + "🕞\n"
            info += "\n" + "🌡 : " + str(self.OutsideTempW)[:4] + "C 💧 : " + str(self.OutSideHumidityW)[:4] + "%\n"
            info += "\n🕋 Sobh :       " + self.AzanMorning + " " + str(self.AzanSobh) + "\n"
            info += "🕋 Zohr :        " + self.AzanNoon + " " + str(self.AzanZohr) + "\n"
            info += "🕋 Magherb : " + self.AzanNight + " " + str(self.AzanMaghreb) + "\n"
            info += "Have a good day MAJN :)"
            bot.sendMessage(MAJN_ID, info)

        if (self.SettingTabAIB):
            if(GPIO.input(16) and self.RoomTabBTN1Bool is False):
                self.RoomTabBTN1ON.click()
            elif(GPIO.input(16) is False and self.RoomTabBTN1Bool):
                self.RoomTabBTN1ON.click()

    def AlarmDef(self):
        now = datetime.now()
        pygame.init()
        if(pygame.mixer.music.get_busy() == False and self.AzanPlaying):
            self.msgBox.done(0)
            self.StopAzan()
        if(pygame.mixer.music.get_busy() == False and self.AlarmPlaying):
            self.msgBox.done(0)
            self.StopAlarm()
        if ("Azan" != None):
            MorningH = int(self.AzanMorning[:2])
            MorningM = int(self.AzanMorning[3:5])
            MorningS = 0
            NoonH = int(self.AzanNoon[:2])
            NoonM = int(self.AzanNoon[3:5])
            NoonS = 0
            NightH = int(self.AzanNight[:2])
            NightM = int(self.AzanNight[3:5])
            NightS = 0

            if (self.AzanSobh and int(now.hour) == MorningH and int(now.minute) == MorningM and int(now.second) == MorningS and self.AzanPlaying == False):
                self.PauseMusic()
                pygame.init()
                pygame.mixer.music.fadeout
                pygame.mixer.music.load(self.Azan)
                pygame.mixer.music.play()
                self.msgBoxer("Azan sobh",self.StopAzan)
                self.AzanPlaying = True
            if (self.AzanZohr and int(now.hour) == NoonH and int(now.minute) == NoonM and int(
                    now.second) == NoonS and self.AzanPlaying == False):
                self.PauseMusic()
                pygame.init()
                pygame.mixer.music.fadeout
                pygame.mixer.music.load(self.Azan)
                pygame.mixer.music.play()
                self.msgBoxer("Azan zohr",self.StopAzan)
                self.AzanPlaying = True
            if (self.AzanMaghreb and int(now.hour) == NightH and int(now.minute) == NightM and int(
                    now.second) == NightS and self.AzanPlaying == False):
                self.PauseMusic()
                pygame.init()
                pygame.mixer.music.fadeout
                pygame.mixer.music.load(self.Azan)
                pygame.mixer.music.play()

                self.msgBoxer("Azan maghreb",self.StopAzan)

                self.AzanPlaying = True
        if ("Alarm" != None and self.SettingTabAlarmB == True):
            H = int(self.SettingTabH.text())
            M = int(self.SettingTabM.text())
            S = int(self.SettingTabS.text())
            sat = self.SettingTabSaturdayB
            sun = self.SettingTabSundayB
            mon = self.SettingTabMondayB
            tue = self.SettingTabTuesdayB
            wed = self.SettingTabWednesdayB
            thu = self.SettingTabThursdayB
            fri = self.SettingTabFridayB
            if (sat == True):
                if (now.strftime("%A") == "Saturday" and int(now.second) == S and int(now.minute) == M and int(
                        now.hour) == H):
                    self.PauseMusic()
                    pygame.init()
                    pygame.mixer.music.fadeout
                    pygame.mixer.music.load(self.AlarmPath)
                    pygame.mixer.music.play()
                    self.AlarmPlaying = True
                    self.RoomTabBTN3ON.click()
                    self.RoomTabBTN1ON.click()
                    self.msgBoxer("Alarm", self.StopAlarm)
            if (sun == True):
                if (now.strftime("%A") == "Sunday" and int(now.second) == S and int(now.minute) == M and int(
                        now.hour) == H):
                    self.PauseMusic()
                    pygame.init()
                    pygame.mixer.music.fadeout
                    pygame.mixer.music.load(self.AlarmPath)
                    pygame.mixer.music.play()
                    self.AlarmPlaying = True
                    self.RoomTabBTN3ON.click()
                    self.RoomTabBTN1ON.click()
                    self.msgBoxer("Alarm", self.StopAlarm)
            if (mon == True):
                if (now.strftime("%A") == "Monday" and int(now.second) == S and int(now.minute) == M and int(
                        now.hour) == H):
                    self.PauseMusic()
                    pygame.init()
                    pygame.mixer.music.fadeout
                    pygame.mixer.music.load(self.AlarmPath)
                    pygame.mixer.music.play()
                    self.AlarmPlaying = True
                    self.RoomTabBTN3ON.click()
                    self.RoomTabBTN1ON.click()
                    self.msgBoxer("Alarm", self.StopAlarm)
            if (tue == True):
                if (now.strftime("%A") == "Tuesday" and int(now.second) == S and int(now.minute) == M and int(
                        now.hour) == H):
                    self.PauseMusic()
                    pygame.init()
                    pygame.mixer.music.fadeout
                    pygame.mixer.music.load(self.AlarmPath)
                    pygame.mixer.music.play()
                    self.AlarmPlaying = True
                    self.RoomTabBTN3ON.click()
                    self.RoomTabBTN1ON.click()
                    self.msgBoxer("Alarm", self.StopAlarm)
            if (wed == True):
                if (now.strftime("%A") == "Wednesday" and int(now.second) == S and int(now.minute) == M and int(
                        now.hour) == H):
                    self.PauseMusic()
                    pygame.init()
                    pygame.mixer.music.fadeout
                    pygame.mixer.music.load(self.AlarmPath)
                    pygame.mixer.music.play()
                    self.AlarmPlaying = True
                    self.RoomTabBTN3ON.click()
                    self.RoomTabBTN1ON.click()
                    self.msgBoxer("Alarm", self.StopAlarm)
            if (thu == True):
                if (now.strftime("%A") == "Thursday" and int(now.second) == S and int(now.minute) == M and int(
                        now.hour) == H):
                    self.PauseMusic()
                    pygame.init()
                    pygame.mixer.music.fadeout
                    pygame.mixer.music.load(self.AlarmPath)
                    pygame.mixer.music.play()
                    self.AlarmPlaying = True
                    self.RoomTabBTN3ON.click()
                    self.RoomTabBTN1ON.click()
                    self.msgBoxer("Alarm", self.StopAlarm)
            if (fri == True):
                if (now.strftime("%A") == "Friday" and int(now.second) == S and int(now.minute) == M and int(
                        now.hour) == H):
                    self.PauseMusic()
                    pygame.init()
                    pygame.mixer.music.fadeout
                    pygame.mixer.music.load(self.AlarmPath)
                    pygame.mixer.music.play()
                    self.AlarmPlaying = True
                    self.RoomTabBTN3ON.click()
                    self.RoomTabBTN1ON.click()
                    self.msgBoxer("Alarm", self.StopAlarm)

    def msgBoxer(self,text,do):
        self.msgBox.setText("<h1>"+text+"</h1>")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.buttonClicked.connect(do)
        self.msgBox.show()

    def StopAzan(self):
        self.AzanPlaying = False
        pygame.init()
        pygame.mixer.music.pause()
        self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
        self.PauseMusic()
        if (self.MusicPlaying == True):
            self.UnpauseMusic()
        return

    def StopAlarm(self):
        self.AlarmPlaying = False
        pygame.init()
        pygame.mixer.music.pause()
        self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
        self.PauseMusic()
        if (self.MusicPlaying == True):
            self.UnpauseMusic()
        return

    def HomeDefAnim(self):
        self.Clicked = True
        self.HomeTabDefAnim1 = QPropertyAnimation(self.HomeTabWidget, b"pos")
        self.HomeTabDefAnim1.setEndValue(QPointF(774, 50))
        self.HomeTabDefAnim1.setDuration(500)
        self.HomeTabDefAnim1.setEasingCurve(QEasingCurve.OutQuart)
        self.HomeTabDefAnim1.start()
        self.HomeTabDefAnim2 = QPropertyAnimation(self.RoomTabWidget, b"pos")
        self.HomeTabDefAnim2.setEndValue(QPointF(1024, 50))
        self.HomeTabDefAnim2.setDuration(500)
        self.HomeTabDefAnim2.setEasingCurve(QEasingCurve.OutQuart)
        self.HomeTabDefAnim2.start()
        self.HomeTabDefAnim3 = QPropertyAnimation(self.TempCoWidget, b"pos")
        self.HomeTabDefAnim3.setEndValue(QPointF(1024, 50))
        self.HomeTabDefAnim3.setDuration(500)
        self.HomeTabDefAnim3.setEasingCurve(QEasingCurve.OutQuart)
        self.HomeTabDefAnim3.start()
        self.HomeTabDefAnim4 = QPropertyAnimation(self.MusicTabWidget, b"pos")
        self.HomeTabDefAnim4.setEndValue(QPointF(1024, 125))
        self.HomeTabDefAnim4.setDuration(500)
        self.HomeTabDefAnim4.setEasingCurve(QEasingCurve.OutQuart)
        self.HomeTabDefAnim4.start()
        self.HomeTabDefAnim5 = QPropertyAnimation(self.SocialTabWidget, b"pos")
        self.HomeTabDefAnim5.setEndValue(QPointF(1024, 50))
        self.HomeTabDefAnim5.setDuration(500)
        self.HomeTabDefAnim5.setEasingCurve(QEasingCurve.OutQuart)
        self.HomeTabDefAnim5.start()
        self.HomeTabDefAnim6 = QPropertyAnimation(self.SettingWidget, b"pos")
        self.HomeTabDefAnim6.setEndValue(QPointF(1024, 75))
        self.HomeTabDefAnim6.setDuration(500)
        self.HomeTabDefAnim6.setEasingCurve(QEasingCurve.OutQuart)
        self.HomeTabDefAnim6.start()

    def RoomDefAnim(self):
        self.Clicked = True
        self.RoomTabDefAnim1 = QPropertyAnimation(self.HomeTabWidget, b"pos")
        self.RoomTabDefAnim1.setEndValue(QPointF(1024, 50))
        self.RoomTabDefAnim1.setDuration(500)
        self.RoomTabDefAnim1.setEasingCurve(QEasingCurve.OutQuart)
        self.RoomTabDefAnim1.start()
        self.RoomTabDefAnim2 = QPropertyAnimation(self.RoomTabWidget, b"pos")
        self.RoomTabDefAnim2.setEndValue(QPointF(274, 50))
        self.RoomTabDefAnim2.setDuration(500)
        self.RoomTabDefAnim2.setEasingCurve(QEasingCurve.OutQuart)
        self.RoomTabDefAnim2.start()
        self.RoomTabDefAnim3 = QPropertyAnimation(self.TempCoWidget, b"pos")
        self.RoomTabDefAnim3.setEndValue(QPointF(1024, 50))
        self.RoomTabDefAnim3.setDuration(500)
        self.RoomTabDefAnim3.setEasingCurve(QEasingCurve.OutQuart)
        self.RoomTabDefAnim3.start()
        self.RoomTabDefAnim4 = QPropertyAnimation(self.MusicTabWidget, b"pos")
        self.RoomTabDefAnim4.setEndValue(QPointF(1024, 125))
        self.RoomTabDefAnim4.setDuration(500)
        self.RoomTabDefAnim4.setEasingCurve(QEasingCurve.OutQuart)
        self.RoomTabDefAnim4.start()
        self.RoomTabDefAnim5 = QPropertyAnimation(self.SocialTabWidget, b"pos")
        self.RoomTabDefAnim5.setEndValue(QPointF(1024, 50))
        self.RoomTabDefAnim5.setDuration(500)
        self.RoomTabDefAnim5.setEasingCurve(QEasingCurve.OutQuart)
        self.RoomTabDefAnim5.start()
        self.RoomTabDefAnim6 = QPropertyAnimation(self.SettingWidget, b"pos")
        self.RoomTabDefAnim6.setEndValue(QPointF(1024, 75))
        self.RoomTabDefAnim6.setDuration(500)
        self.RoomTabDefAnim6.setEasingCurve(QEasingCurve.OutQuart)
        self.RoomTabDefAnim6.start()

    def TempCoDefAnim(self):
        self.Clicked = True
        self.TempCoTabDefAnim1 = QPropertyAnimation(self.HomeTabWidget, b"pos")
        self.TempCoTabDefAnim1.setEndValue(QPointF(1024, 50))
        self.TempCoTabDefAnim1.setDuration(500)
        self.TempCoTabDefAnim1.setEasingCurve(QEasingCurve.OutQuart)
        self.TempCoTabDefAnim1.start()
        self.TempCoTabDefAnim2 = QPropertyAnimation(self.RoomTabWidget, b"pos")
        self.TempCoTabDefAnim2.setEndValue(QPointF(1024, 50))
        self.TempCoTabDefAnim2.setDuration(500)
        self.TempCoTabDefAnim2.setEasingCurve(QEasingCurve.OutQuart)
        self.TempCoTabDefAnim2.start()
        self.TempCoTabDefAnim3 = QPropertyAnimation(self.TempCoWidget, b"pos")
        self.TempCoTabDefAnim3.setEndValue(QPointF(474, 50))
        self.TempCoTabDefAnim3.setDuration(500)
        self.TempCoTabDefAnim3.setEasingCurve(QEasingCurve.OutQuart)
        self.TempCoTabDefAnim3.start()
        self.TempCoTabDefAnim4 = QPropertyAnimation(self.MusicTabWidget, b"pos")
        self.TempCoTabDefAnim4.setEndValue(QPointF(1024, 125))
        self.TempCoTabDefAnim4.setDuration(500)
        self.TempCoTabDefAnim4.setEasingCurve(QEasingCurve.OutQuart)
        self.TempCoTabDefAnim4.start()
        self.TempCoTabDefAnim5 = QPropertyAnimation(self.SocialTabWidget, b"pos")
        self.TempCoTabDefAnim5.setEndValue(QPointF(1024, 50))
        self.TempCoTabDefAnim5.setDuration(500)
        self.TempCoTabDefAnim5.setEasingCurve(QEasingCurve.OutQuart)
        self.TempCoTabDefAnim5.start()
        self.TempCoTabDefAnim6 = QPropertyAnimation(self.SettingWidget, b"pos")
        self.TempCoTabDefAnim6.setEndValue(QPointF(1024, 75))
        self.TempCoTabDefAnim6.setDuration(500)
        self.TempCoTabDefAnim6.setEasingCurve(QEasingCurve.OutQuart)
        self.TempCoTabDefAnim6.start()

    def MusicDefAnim(self):
        self.Clicked = True
        self.MusicTabDefAnim1 = QPropertyAnimation(self.HomeTabWidget, b"pos")
        self.MusicTabDefAnim1.setEndValue(QPointF(1024, 50))
        self.MusicTabDefAnim1.setDuration(500)
        self.MusicTabDefAnim1.setEasingCurve(QEasingCurve.OutQuart)
        self.MusicTabDefAnim1.start()
        self.MusicTabDefAnim2 = QPropertyAnimation(self.RoomTabWidget, b"pos")
        self.MusicTabDefAnim2.setEndValue(QPointF(1024, 50))
        self.MusicTabDefAnim2.setDuration(500)
        self.MusicTabDefAnim2.setEasingCurve(QEasingCurve.OutQuart)
        self.MusicTabDefAnim2.start()
        self.MusicTabDefAnim3 = QPropertyAnimation(self.TempCoWidget, b"pos")
        self.MusicTabDefAnim3.setEndValue(QPointF(1024, 50))
        self.MusicTabDefAnim3.setDuration(500)
        self.MusicTabDefAnim3.setEasingCurve(QEasingCurve.OutQuart)
        self.MusicTabDefAnim3.start()
        self.MusicTabDefAnim4 = QPropertyAnimation(self.MusicTabWidget, b"pos")
        self.MusicTabDefAnim4.setEndValue(QPointF(674, 125))
        self.MusicTabDefAnim4.setDuration(500)
        self.MusicTabDefAnim4.setEasingCurve(QEasingCurve.OutQuart)
        self.MusicTabDefAnim4.start()
        self.MusicTabDefAnim5 = QPropertyAnimation(self.SocialTabWidget, b"pos")
        self.MusicTabDefAnim5.setEndValue(QPointF(1024, 50))
        self.MusicTabDefAnim5.setDuration(500)
        self.MusicTabDefAnim5.setEasingCurve(QEasingCurve.OutQuart)
        self.MusicTabDefAnim5.start()
        self.MusicTabDefAnim6 = QPropertyAnimation(self.SettingWidget, b"pos")
        self.MusicTabDefAnim6.setEndValue(QPointF(1024, 75))
        self.MusicTabDefAnim6.setDuration(500)
        self.MusicTabDefAnim6.setEasingCurve(QEasingCurve.OutQuart)
        self.MusicTabDefAnim6.start()

    def SocialDefAnim(self):
        self.Clicked = True
        self.SocialTabDefAnim1 = QPropertyAnimation(self.HomeTabWidget, b"pos")
        self.SocialTabDefAnim1.setEndValue(QPointF(1024, 50))
        self.SocialTabDefAnim1.setDuration(500)
        self.SocialTabDefAnim1.setEasingCurve(QEasingCurve.OutQuart)
        self.SocialTabDefAnim1.start()
        self.SocialTabDefAnim2 = QPropertyAnimation(self.RoomTabWidget, b"pos")
        self.SocialTabDefAnim2.setEndValue(QPointF(1024, 50))
        self.SocialTabDefAnim2.setDuration(500)
        self.SocialTabDefAnim2.setEasingCurve(QEasingCurve.OutQuart)
        self.SocialTabDefAnim2.start()
        self.SocialTabDefAnim3 = QPropertyAnimation(self.TempCoWidget, b"pos")
        self.SocialTabDefAnim3.setEndValue(QPointF(1024, 50))
        self.SocialTabDefAnim3.setDuration(500)
        self.SocialTabDefAnim3.setEasingCurve(QEasingCurve.OutQuart)
        self.SocialTabDefAnim3.start()
        self.SocialTabDefAnim4 = QPropertyAnimation(self.MusicTabWidget, b"pos")
        self.SocialTabDefAnim4.setEndValue(QPointF(1024, 125))
        self.SocialTabDefAnim4.setDuration(500)
        self.SocialTabDefAnim4.setEasingCurve(QEasingCurve.OutQuart)
        self.SocialTabDefAnim4.start()
        self.SocialTabDefAnim5 = QPropertyAnimation(self.SocialTabWidget, b"pos")
        self.SocialTabDefAnim5.setEndValue(QPointF(274, 50))
        self.SocialTabDefAnim5.setDuration(500)
        self.SocialTabDefAnim5.setEasingCurve(QEasingCurve.OutQuart)
        self.SocialTabDefAnim5.start()
        self.SocialTabDefAnim6 = QPropertyAnimation(self.SettingWidget, b"pos")
        self.SocialTabDefAnim6.setEndValue(QPointF(1024, 75))
        self.SocialTabDefAnim6.setDuration(500)
        self.SocialTabDefAnim6.setEasingCurve(QEasingCurve.OutQuart)
        self.SocialTabDefAnim6.start()

    def SettingDefAnim(self):
        self.Clicked = True
        self.SettingTabDefAnim1 = QPropertyAnimation(self.HomeTabWidget, b"pos")
        self.SettingTabDefAnim1.setEndValue(QPointF(1024, 50))
        self.SettingTabDefAnim1.setDuration(500)
        self.SettingTabDefAnim1.setEasingCurve(QEasingCurve.OutQuart)
        self.SettingTabDefAnim1.start()
        self.SettingTabDefAnim2 = QPropertyAnimation(self.RoomTabWidget, b"pos")
        self.SettingTabDefAnim2.setEndValue(QPointF(1024, 50))
        self.SettingTabDefAnim2.setDuration(500)
        self.SettingTabDefAnim2.setEasingCurve(QEasingCurve.OutQuart)
        self.SettingTabDefAnim2.start()
        self.SettingTabDefAnim3 = QPropertyAnimation(self.TempCoWidget, b"pos")
        self.SettingTabDefAnim3.setEndValue(QPointF(1024, 50))
        self.SettingTabDefAnim3.setDuration(500)
        self.SettingTabDefAnim3.setEasingCurve(QEasingCurve.OutQuart)
        self.SettingTabDefAnim3.start()
        self.SettingTabDefAnim4 = QPropertyAnimation(self.MusicTabWidget, b"pos")
        self.SettingTabDefAnim4.setEndValue(QPointF(1024, 125))
        self.SettingTabDefAnim4.setDuration(500)
        self.SettingTabDefAnim4.setEasingCurve(QEasingCurve.OutQuart)
        self.SettingTabDefAnim4.start()
        self.SettingTabDefAnim5 = QPropertyAnimation(self.SocialTabWidget, b"pos")
        self.SettingTabDefAnim5.setEndValue(QPointF(1024, 50))
        self.SettingTabDefAnim5.setDuration(500)
        self.SettingTabDefAnim5.setEasingCurve(QEasingCurve.OutQuart)
        self.SettingTabDefAnim5.start()
        self.SettingTabDefAnim6 = QPropertyAnimation(self.SettingWidget, b"pos")
        self.SettingTabDefAnim6.setEndValue(QPointF(274, 75))
        self.SettingTabDefAnim6.setDuration(500)
        self.SettingTabDefAnim6.setEasingCurve(QEasingCurve.OutQuart)
        self.SettingTabDefAnim6.start()

    def ClockHomeDef(self):
        now = datetime.now()
        if (self.HomeState == "Home"):
            self.HomeTabClockH.setText(str(int(now.hour)))
            self.HomeTabClockM.setText(now.strftime("%M"))
            self.HomeTabClockS.setText(now.strftime("%S"))
            self.HomeTabDay.setText(now.strftime("%A"))
            self.HomeTabDate.setText(str(now.day) + "  " + str(now.strftime("%B")) + "  " + str(now.year))
        if (self.HomeState == "Room"):
            self.RoomTabClockH.setText(str(int(now.hour)))
            self.RoomTabClockM.setText(now.strftime("%M"))
            self.RoomTabClockS.setText(now.strftime("%S"))
            if (now.hour == 0 and now.minute == 0 and now.second == 0):
                weather = str(
                    urllib3.PoolManager().request('GET',
                                                  'https://www.google.com/search?q=tehran+weather&oq=tehran+weather').data)
                weatherL = weather.find("<span class=\"today-daypart-wxphrase\" id=\"dp0-phrase\">") + len(
                    "<span class=\"today-daypart-wxphrase\" id=\"dp0-phrase\">")
                weather = weather[weatherL:]
                self.weather = weather[0: weather.find("</span></div>")]

    def RoomTabBTN1Def(self):
        now = datetime.now()
        self.Clicked = True
        self.RoomTabBTN1Bool = not self.RoomTabBTN1Bool
        if (self.RoomTabBTN1Bool == True):
            self.FadeOutIn(self.RoomTabBTN1LabelOFF, 0, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN1LabelON, 1, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN1OFF, 2, 0.3, 0)
            self.FadeOutIn(self.RoomTabBTN1ON, 3, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN1Label2, 4, 0, 0.6)
            if(int(now.hour) > int(self.AzanMorning[:2]) and int(now.hour) < int(self.AzanNight[:2]) and (self.ANNH[now.hour] < 120)):
                self.ANNH[now.hour] += 20
            elif(self.ANNH[now.hour] < 120):
                self.ANNH[now.hour] += 40
        if (self.RoomTabBTN1Bool == False):
            self.FadeOutIn(self.RoomTabBTN1LabelOFF, 6, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN1LabelON, 7, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN1OFF, 8, 0, 0.3)
            self.FadeOutIn(self.RoomTabBTN1ON, 9, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN1Label2, 10, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN1Label3, 11, 0.6, 0)
            if(int(now.hour) > int(self.AzanMorning[:2]) and int(now.hour) < int(self.AzanNight[:2]) and self.ANNH[now.hour] > -20):
                self.ANNH[now.hour] -= 40
            elif(self.ANNH[now.hour] > -20):
                self.ANNH[now.hour] -= 20
        # ! GPIO.output(6, self.RoomTabBTN1Bool)

    def RoomTabBTN2Def(self):
        self.Clicked = True
        self.RoomTabBTN2Bool = not self.RoomTabBTN2Bool
        if (self.RoomTabBTN2Bool == True):
            self.FadeOutIn(self.RoomTabBTN2LabelOFF, 12, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN2LabelON, 13, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN2OFF, 14, 0.3, 0)
            self.FadeOutIn(self.RoomTabBTN2ON, 15, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN2Label2, 16, 0, 0.6)
            # self.FadeOutIn(self.RoomTabBTN1Label3,   5, 0, 0.6)
        if (self.RoomTabBTN2Bool == False):
            self.FadeOutIn(self.RoomTabBTN2LabelOFF, 17, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN2LabelON, 18, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN2OFF, 19, 0, 0.3)
            self.FadeOutIn(self.RoomTabBTN2ON, 20, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN2Label2, 21, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN2Label3, 22, 0.6, 0)
        # ! GPIO.output(27, self.RoomTabBTN2Bool)

    def RoomTabBTN3Def(self):
        self.Clicked = True
        self.RoomTabBTN3Bool = not self.RoomTabBTN3Bool
        if (self.RoomTabBTN3Bool == True):
            self.FadeOutIn(self.RoomTabBTN3LabelOFF, 23, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN3LabelON, 24, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN3OFF, 25, 0.3, 0)
            self.FadeOutIn(self.RoomTabBTN3ON, 26, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN3Label2, 27, 0, 0.6)
            # self.FadeOutIn(self.RoomTabBTN1Label3,   5, 0, 0.6)
        if (self.RoomTabBTN3Bool == False):
            self.FadeOutIn(self.RoomTabBTN3LabelOFF, 28, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN3LabelON, 29, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN3OFF, 30, 0, 0.3)
            self.FadeOutIn(self.RoomTabBTN3ON, 31, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN3Label2, 32, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN3Label3, 33, 0.6, 0)
        # ! GPIO.output(22, self.RoomTabBTN3Bool)

    def RoomTabBTN4Def(self):
        self.Clicked = True
        self.RoomTabBTN4Bool = not self.RoomTabBTN4Bool
        if (self.RoomTabBTN4Bool == True):
            self.FadeOutIn(self.RoomTabBTN4LabelOFF, 34, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN4LabelON, 35, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN4OFF, 36, 0.3, 0)
            self.FadeOutIn(self.RoomTabBTN4ON, 37, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN4Label2, 38, 0, 0.6)
            # self.FadeOutIn(self.RoomTabBTN1Label3,   5, 0, 0.6)
        if (self.RoomTabBTN4Bool == False):
            self.FadeOutIn(self.RoomTabBTN4LabelOFF, 39, 0, 0.6)
            self.FadeOutIn(self.RoomTabBTN4LabelON, 40, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN4OFF, 41, 0, 0.3)
            self.FadeOutIn(self.RoomTabBTN4ON, 42, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN4Label2, 43, 0.6, 0)
            self.FadeOutIn(self.RoomTabBTN4Label3, 44, 0.6, 0)
        # ! GPIO.output(19, self.RoomTabBTN4Bool)

    def RoomTabBTNsDef(self):
        if (self.HomeState == "Room"):

            if (self.RoomTabBTN1Bool == True):
                self.FadeTimerHomeDef(self.RoomTabBTN1Label2, 0, 0.6, 0)
                self.FadeTimerHomeDef(self.RoomTabBTN1Label3, 1, 0, 0.6)
            if (self.RoomTabBTN2Bool == True):
                self.FadeTimerHomeDef(self.RoomTabBTN2Label2, 2, 0.6, 0)
                self.FadeTimerHomeDef(self.RoomTabBTN2Label3, 3, 0, 0.6)
            if (self.RoomTabBTN3Bool == True):
                self.FadeTimerHomeDef(self.RoomTabBTN3Label2, 4, 0.6, 0)
                self.FadeTimerHomeDef(self.RoomTabBTN3Label3, 5, 0, 0.6)
            if (self.RoomTabBTN4Bool == True):
                self.FadeTimerHomeDef(self.RoomTabBTN4Label2, 6, 0.6, 0)
                self.FadeTimerHomeDef(self.RoomTabBTN4Label3, 7, 0, 0.6)

    def TempCoTabAutoUpBTNDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.TempCoTabAutoUpBTN, 1, 0.5, 1)
        self.FadeUpFadeDown(self.TempCoTabAutoInsideTempLabel, 2, 0.3, 0.1)
        if (int(self.TempCoTabAutoInsideTempTXT.text()) <= 31):
            self.TempCoTabAutoInsideTempTXT.setText(str(int(self.TempCoTabAutoInsideTempTXT.text()) + 1))

    def TempCoTabAutoDownBTNDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.TempCoTabAutoDownBTN, 3, 0.5, 1)
        self.FadeUpFadeDown(self.TempCoTabAutoInsideTempLabel, 4, 0.3, 0.1)
        if (int(self.TempCoTabAutoInsideTempTXT.text()) >= 19):
            self.TempCoTabAutoInsideTempTXT.setText(str(int(self.TempCoTabAutoInsideTempTXT.text()) - 1))

    def SettingTabHUpDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.SettingTabHUp, 5, 0.3, 0.6)
        self.FadeUpFadeDown(self.SettingTabH, 6, 0.7, 0.4)
        if (int(self.SettingTabH.text()) < 23):
            self.SettingTabH.setText(str(int(self.SettingTabH.text()) + 1))

    def SettingTabHDownDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.SettingTabHDown, 7, 0.3, 0.6)
        self.FadeUpFadeDown(self.SettingTabH, 8, 0.7, 0.4)
        if (int(self.SettingTabH.text()) > 0):
            self.SettingTabH.setText(str(int(self.SettingTabH.text()) - 1))

    def SettingTabMUpDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.SettingTabMUp, 9, 0.3, 0.6)
        self.FadeUpFadeDown(self.SettingTabM, 10, 0.7, 0.4)
        if (int(self.SettingTabM.text()) < 55):
            self.SettingTabM.setText(str(int(self.SettingTabM.text()) + 5))

    def SettingTabMDownDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.SettingTabMDown, 11, 0.3, 0.6)
        self.FadeUpFadeDown(self.SettingTabM, 12, 0.7, 0.4)
        if (int(self.SettingTabM.text()) > 0):
            self.SettingTabM.setText(str(int(self.SettingTabM.text()) - 5))

    def SettingTabSUpDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.SettingTabSUp, 13, 0.3, 0.6)
        self.FadeUpFadeDown(self.SettingTabS, 14, 0.7, 0.4)
        if (int(self.SettingTabS.text()) < 55):
            self.SettingTabS.setText(str(int(self.SettingTabS.text()) + 5))

    def SettingTabSDownDef(self):
        self.Clicked = True
        self.FadeUpFadeDown(self.SettingTabSDown, 15, 0.3, 0.6)
        self.FadeUpFadeDown(self.SettingTabS, 16, 0.7, 0.4)
        if (int(self.SettingTabS.text()) < 59):
            self.SettingTabS.setText(str(int(self.SettingTabS.text()) - 5))

    def SettingTabSaveCamDef(self):
        self.Clicked = True
        self.SettingTabSaveCamPath = str(
            QFileDialog.getExistingDirectory(self, "Select Your Directory For Save Cam's Photos"))
        self.SettingTabSaveCamPath = self.SettingTabSaveCamPath.replace('\\', '/')
        self.SettingTabSaveCamPath += '/'

    def SettingTabAlarmDef(self):
        self.Clicked = True
        self.SettingTabAlarmB = not self.SettingTabAlarmB
        if (self.SettingTabAlarmB == True):
            self.SettingTabAlarmAnim.setStartValue(750, 250, 750, 200)
            self.SettingTabAlarmAnim.setEndValue(0, 250, 750, 200)
            self.SettingTabAlarmAnim.setDuration(500)
            self.SettingTabAlarmAnim.start()
            self.ChangeImageFading(self.SettingTabAlarm, 15, 0.4, "Label/Setting/AlarmON.png")
        else:
            self.SettingTabAlarmAnim.setStartValue(0, 250, 750, 200)
            self.SettingTabAlarmAnim.setEndValue(750, 250, 750, 200)
            self.SettingTabAlarmAnim.setDuration(500)
            self.SettingTabAlarmAnim.start()
            self.ChangeImageFading(self.SettingTabAlarm, 16, 0.4, "Label/Setting/AlarmOFF.png")

    def SettingTabSaturdayDef(self):
        self.SettingTabSaturdayB = not self.SettingTabSaturdayB
        if (self.SettingTabSaturdayB == True):
            self.ChangeImageFading(self.SettingTabSaturday, 17, 0.4, "Label/Setting/SON.png")
        else:
            self.ChangeImageFading(self.SettingTabSaturday, 18, 0.4, "Label/Setting/SOFF.png")

    def SettingTabSundayDef(self):
        self.SettingTabSundayB = not self.SettingTabSundayB
        if (self.SettingTabSundayB == True):
            self.ChangeImageFading(self.SettingTabSunday, 19, 0.4, "Label/Setting/SON.png")
        else:
            self.ChangeImageFading(self.SettingTabSunday, 20, 0.4, "Label/Setting/SOFF.png")

    def SettingTabMondayDef(self):
        self.SettingTabMondayB = not self.SettingTabMondayB
        if (self.SettingTabMondayB == True):
            self.ChangeImageFading(self.SettingTabMonday, 21, 0.4,
                                   "Label/Setting/MON.png")
        else:
            self.ChangeImageFading(self.SettingTabMonday, 22, 0.4,
                                   "Label/Setting/MOFF.png")

    def SettingTabTuesdayDef(self):
        self.SettingTabTuesdayB = not self.SettingTabTuesdayB
        if (self.SettingTabTuesdayB == True):
            self.ChangeImageFading(self.SettingTabTuesday, 23, 0.4,
                                   "Label/Setting/TON.png")
        else:
            self.ChangeImageFading(self.SettingTabTuesday, 24, 0.4,
                                   "Label/Setting/TOFF.png")

    def SettingTabWednesdayDef(self):
        self.SettingTabWednesdayB = not self.SettingTabWednesdayB
        if (self.SettingTabWednesdayB == True):
            self.ChangeImageFading(self.SettingTabWednesday, 25, 0.4,
                                   "Label/Setting/WON.png")
        else:
            self.ChangeImageFading(self.SettingTabWednesday, 26, 0.4,
                                   "Label/Setting/WOFF.png")

    def SettingTabThursdayDef(self):
        self.SettingTabThursdayB = not self.SettingTabThursdayB
        if (self.SettingTabThursdayB == True):
            self.ChangeImageFading(self.SettingTabThursday, 27, 0.4,
                                   "Label/Setting/TON.png")
        else:
            self.ChangeImageFading(self.SettingTabThursday, 28, 0.4,
                                   "Label/Setting/TOFF.png")

    def SettingTabFridayDef(self):
        self.SettingTabFridayB = not self.SettingTabFridayB
        if (self.SettingTabFridayB == True):
            self.ChangeImageFading(self.SettingTabFriday, 29, 0.4,
                                   "Label/Setting/FON.png")
        else:
            self.ChangeImageFading(self.SettingTabFriday, 30, 0.4,
                                   "Label/Setting/FOFF.png")

    def SettingTabAIDef(self):
        self.Clicked = True
        self.SettingTabAIB = not self.SettingTabAIB
        if (self.SettingTabAIB == True):
            self.ChangeImageFading(self.SettingTabAI, 31, 0.4, "Label/Setting/AION.png")
        else:
            self.ChangeImageFading(self.SettingTabAI, 32, 0.4, "Label/Setting/AIOFF.png")

    def TempCoModeDef(self):
        self.TempCoTabModeBool = not self.TempCoTabModeBool
        if (self.TempCoTabModeBool == True):  # Manual
            self.TempCoModeAnim = QPropertyAnimation(self.TempCoTabModeLabel1, 'pos')
            self.TempCoModeAnim.setStartValue(QPoint(20, 19))
            self.TempCoModeAnim.setEndValue(QPoint(20, 81))
            self.TempCoModeAnim.start()
            self.TempCoTabManualWidgetAnim = QPropertyAnimation(self.TempCoTabManualWidget, 'pos')
            self.TempCoTabManualWidgetAnim.setStartValue(QPoint(550, 300))
            self.TempCoTabManualWidgetAnim.setEndValue(QPoint(250, 300))
            self.TempCoTabManualWidgetAnim.start()
            self.TempCoModeAnim.start()
            self.TempCoTabAutoWidgetAnim = QPropertyAnimation(self.TempCoTabAutoWidget, 'pos')
            self.TempCoTabAutoWidgetAnim.setStartValue(QPoint(215, 300))
            self.TempCoTabAutoWidgetAnim.setEndValue(QPoint(550, 300))
            self.TempCoTabAutoWidgetAnim.start()
        if (self.TempCoTabModeBool == False):  # Manual
            self.TempCoModeAnim = QPropertyAnimation(self.TempCoTabModeLabel1, 'pos')
            self.TempCoModeAnim.setStartValue(QPoint(20, 81))
            self.TempCoModeAnim.setEndValue(QPoint(20, 19))
            self.TempCoModeAnim.start()
            self.TempCoTabManualWidgetAnim = QPropertyAnimation(self.TempCoTabManualWidget, 'pos')
            self.TempCoTabManualWidgetAnim.setStartValue(QPoint(250, 300))
            self.TempCoTabManualWidgetAnim.setEndValue(QPoint(550, 300))
            self.TempCoTabManualWidgetAnim.start()
            self.TempCoModeAnim.start()
            self.TempCoTabAutoWidgetAnim = QPropertyAnimation(self.TempCoTabAutoWidget, 'pos')
            self.TempCoTabAutoWidgetAnim.setStartValue(QPoint(550, 300))
            self.TempCoTabAutoWidgetAnim.setEndValue(QPoint(215, 300))
            self.TempCoTabAutoWidgetAnim.start()

    def TempCoTabManualTurnDef(self):
        self.TempCoTabManualTurnBool = not self.TempCoTabManualTurnBool
        if (self.TempCoTabManualTurnBool == True):  # Manual
            self.TempCoManualTurnAnim = QPropertyAnimation(self.TempCoTabManualTurnLabel, 'pos')
            self.TempCoManualTurnAnim.setStartValue(QPoint(125, 77))
            self.TempCoManualTurnAnim.setEndValue(QPoint(125, 23))
            self.TempCoManualTurnAnim.start()
        if (self.TempCoTabManualTurnBool == False):  # Manual
            self.TempCoManualTurnAnim = QPropertyAnimation(self.TempCoTabManualTurnLabel, 'pos')
            self.TempCoManualTurnAnim.setStartValue(QPoint(125, 23))
            self.TempCoManualTurnAnim.setEndValue(QPoint(125, 77))
            self.TempCoManualTurnAnim.start()

    def TempCoTabManualSpeedDef(self):
        self.TempCoTabManualSpeedBool = not self.TempCoTabManualSpeedBool
        if (self.TempCoTabManualSpeedBool == True):  # Manual
            self.TempCoManualSpeedAnim = QPropertyAnimation(self.TempCoTabManualSpeedLabel, 'pos')
            self.TempCoManualSpeedAnim.setStartValue(QPoint(29, 77))
            self.TempCoManualSpeedAnim.setEndValue(QPoint(29, 23))
            self.TempCoManualSpeedAnim.start()
        if (self.TempCoTabManualSpeedBool == False):  # Manual
            self.TempCoManualSpeedAnim = QPropertyAnimation(self.TempCoTabManualSpeedLabel, 'pos')
            self.TempCoManualSpeedAnim.setStartValue(QPoint(29, 23))
            self.TempCoManualSpeedAnim.setEndValue(QPoint(29, 77))
            self.TempCoManualSpeedAnim.start()

    def TempCheckDef(self):
        now = datetime.now()
        if (int(now.minute) % 14 == 1 and int(now.second) == 5):
            hm, tm = 35, 35 # ! Adafruit_DHT.read_retry(22, 4)
            self.TempCheckAve = tm
            self.HumiCheckAve = hm
            self.TempCoTabAutoOutsideTempTXT.setText(str(int(self.TempCheckAve)))
            for n in range(24):
                if (n == int(now.hour) - 1):
                    self.TempClockInHour[n] = float(tm)
                    self.TempCoTabGraphH[n].setGeometry(
                        53 + n * (454 / 23), 215 - ((self.TempClockInHour[n] - 19) * (185 / 12)), 10,
                                     ((self.TempClockInHour[n] - 19) * (185 / 12)))
                    if (self.TempClockInHour[n] <= 21):
                        self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetL)
                    elif (self.TempClockInHour[n] < 26):
                        self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetM)
                    else:
                        self.TempCoTabGraphH[n].setStyleSheet(self.TempCoSetStyleSheetH)
                    self.TempCoTabGraphH[n].setGraphicsEffect(Opacity(0.4))

    def WeatherCheck(self):
        now = datetime.now()
        if (int(now.minute) % 25 == 0):
            r = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=Tehran&APPID=b3a9cd6b01d2ab3fe9f0187351659781')
            self.HomeTabWeatherLabel.setText(str(r.json()['weather'][0]['description']))
            self.EbrimaFont.setPixelSize(35 - (0.7 * len(str(r.json()['weather'][0]['description']))))
            self.OutsideTempW = str(int(r.json()['main']['temp']) - 273.15)
            self.OutSideHumidityW = str(int(r.json()['main']['humidity']))
        if (int(now.minute) % 2 == 0):
            self.FadeOutIn(self.HomeTabTText, 45, 0.7, 0)
            self.FadeOutIn(self.HomeTabTempText, 46, 0.7, 0)
            self.FadeOutIn(self.HomeTabHumidityText, 47, 0.7, 0)
            self.HomeTabTText.setText("Inside")
            self.HomeTabTempText.setText(str(int(self.TempCheckAve)))
            self.HomeTabHumidityText.setText(str(int(self.HumiCheckAve)))
            self.FadeOutIn(self.HomeTabTText, 48, 0, 0.7)
            self.FadeOutIn(self.HomeTabTempText, 49, 0, 0.7)
            self.FadeOutIn(self.HomeTabHumidityText, 50, 0, 0.7)
        if (int(now.minute) % 2 == 1):
            self.FadeOutIn(self.HomeTabTText, 51, 0.7, 0)
            self.FadeOutIn(self.HomeTabTempText, 52, 0.7, 0)
            self.FadeOutIn(self.HomeTabHumidityText, 53, 0.7, 0)
            self.HomeTabTText.setText("Outside")
            self.HomeTabTempText.setText(self.OutsideTempW[:4])
            self.HomeTabHumidityText.setText(self.OutSideHumidityW[:3])
            self.FadeOutIn(self.HomeTabTText, 54, 0, 0.7)
            self.FadeOutIn(self.HomeTabTempText, 55, 0, 0.7)
            self.FadeOutIn(self.HomeTabHumidityText, 56, 0, 0.7)

    def BGPathDef(self):
        self.FadeUnfade(self.SettingTabTheme, 7)
        self.BGImagesNUM = 0
        self.BGPathL = []
        self.BGPath = str(QFileDialog.getExistingDirectory(self, "Select Your Directory For Wallpapers"))
        self.BGPath = self.BGPath.replace('\\', '/')
        self.BGPath += '/'
        print(self.BGPath)
        for (self.dirpath, self.dirnames, self.filenames) in walk(self.BGPath):
            print(len(self.filenames))
            self.BGPathL.extend(self.filenames)
            break
        BGFile = open("BGPath.txt", 'w')
        BGFile.write(self.BGPath)
        BGFile.close()

    def BGTimerDef(self):
        now = datetime.now()
        if (now.minute % 2 == 0 and now.second % 35 == 0 and self.AzanPlaying == False and self.AlarmPlaying == False):
            self.BGLabel2.setPixmap(QPixmap(self.BGPath + self.BGPathL[self.BGImagesNUM]))
            opacity = QGraphicsOpacityEffect(self)
            self.BGLabel2.setGraphicsEffect(Opacity(1))
            self.BGImagesNUM += 1
            if (self.BGImagesNUM == len(self.filenames) - 1):
                self.BGImagesNUM = 0
            self.BGLabel1.setPixmap(QPixmap(self.BGPath + self.BGPathL[self.BGImagesNUM]))
            opacity1 = QGraphicsOpacityEffect()
            self.BGLabel2.setGraphicsEffect(opacity1)
            self.ChangeBackGroundAnim = QPropertyAnimation(opacity1, b'opacity')
            self.ChangeBackGroundAnim.setDuration(500)
            self.ChangeBackGroundAnim.setStartValue(1)
            self.ChangeBackGroundAnim.setEndValue(0)
            self.ChangeBackGroundAnim.start()
            del opacity1
            del opacity

    def MusicTabFolderDef(self):
        self.MusicPath = str(QFileDialog.getExistingDirectory(self, "Select Your Directory For Music"))
        self.MusicPath = self.MusicPath.replace('\\', '/')
        self.MusicPath += '/'
        print("Music : " + self.MusicPath)
        for (self.Musicdirpath, self.Musicdirnames, self.MusicFileName) in walk(self.MusicPath):
            self.MusicsNUM = len(self.MusicFileName)
            self.MusicPathL.extend(self.MusicFileName)
            break
        MusicFile = open("MusicPath.txt", 'w')
        MusicFile.write(str(self.MusicPath))
        MusicFile.close()
        self.AlarmPath = QFileDialog.getOpenFileName(self, "Open a mp3 file for alarm", "Alarm mp3", " (*.mp3)")
        self.AlarmPath = self.AlarmPath.replace('\\', '/')
        fileCheck1 = open("AlarmPath.txt", "w")
        fileCheck1.write(self.AlarmPath)
        fileCheck1.close()
        self.Azan = QFileDialog.getOpenFileName(self, "Open a mp3 file for Azan", "Azan mp3", " (*.mp3)")
        self.Azan = self.Azan.replace('\\', '/')
        fileCheck1 = open("Azan.txt", "w")
        fileCheck1.write(self.Azan)
        fileCheck1.close()
        self.MusicNumPlaying = 0
        self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
        self.MusicPlaying = False
        self.HomeTabMusicPlay.click()

    def BackMusicDef(self):
        self.Clicked = True
        self.FadeUnfade(self.HomeTabMusicBack, 1)
        self.FadeUnfade(self.MusicTabBack, 2)
        if (self.MusicNumPlaying > 0):
            self.MusicNumPlaying -= 1
        else:
            self.MusicNumPlaying = self.MusicsNUM - 1
        self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
        self.PauseMusic()
        if (self.MusicPlaying == True):
            self.UnpauseMusic()

    def PlayMusicDef(self):
        self.MusicPlaying = not self.MusicPlaying
        self.Clicked = True
        if (self.MusicPlaying == True):
            self.ChangeImageFading(self.HomeTabMusicPlay, 1, 0.4, "Label/pause.png")
            self.ChangeImageFading(self.MusicTabPlay, 2, 0.4, "Label/pause.png")
            self.UnpauseMusic()
        else:
            self.ChangeImageFading(self.HomeTabMusicPlay, 3, 0.4, "Label/play.png")
            self.ChangeImageFading(self.MusicTabPlay, 4, 0.4, "Label/play.png")
            self.PauseMusic()

    def NextMusicDef(self):
        self.Clicked = True
        self.FadeUnfade(self.HomeTabMusicNext, 5)
        self.FadeUnfade(self.MusicTabNext, 6)
        if (self.MusicNumPlaying < self.MusicsNUM - 1):
            self.MusicNumPlaying += 1
        else:
            self.MusicNumPlaying = 0
        self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
        self.PauseMusic()
        if (self.MusicPlaying == True):
            self.UnpauseMusic()

    def MusicTabModeDef(self):
        self.MusicNormalMode = not self.MusicNormalMode
        if (self.MusicNormalMode == True):
            self.ChangeImageFading(self.MusicTabMode, 5, 0.4, "Label/Music/Normal.png")
        else:
            self.ChangeImageFading(self.MusicTabMode, 6, 0.4, "Label/Music/Repeat.png")
        print(self.MusicNormalMode)

    def MusicTimerDef(self):
        if (self.IsPlaying() == False and self.MusicPlaying == True and self.AzanPlaying == False):
            if (self.MusicNormalMode == True):
                if (self.MusicNumPlaying < self.MusicsNUM):
                    self.MusicNumPlaying += 1
                else:
                    self.MusicNumPlaying = 0
                self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
            else:
                self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
        if (self.AzanPlaying == True and self.IsPlaying() == False):
            self.PlayMusic(self.MusicPath + self.MusicFileName[self.MusicNumPlaying])
            self.PauseMusic()
            self.AzanPlaying == False
        T = str(self.MusicFileName[self.MusicNumPlaying])
        Artist = T[0:T.find('-')]
        Name = T[T.find('-') + 2:T.find('.')]
        self.MusicTabNameArtist.setText(Artist)
        self.MusicTabNameMusic.setText(Name)
        self.LastSongName = self.MusicTabNameMusic.text()

    def MusicTabVolumeUpDef(self):
        if (self.MusicVolume < 0.1):
            self.MusicVolume += 0.01
        self.SetVolume(self.MusicVolume)
        if (self.MusicVolume > 0.06):
            self.ChangeImageFading(self.MusicTabVolume, 7, 0.4, "Label/Music/High.png")
        elif (self.MusicVolume > 0.03):
            self.ChangeImageFading(self.MusicTabVolume, 8, 0.4, "Label/Music/Medium.png")
        elif (self.MusicVolume > 0):
            self.ChangeImageFading(self.MusicTabVolume, 9, 0.4, "Label/Music/Low.png")
        else:
            self.ChangeImageFading(self.MusicTabVolume, 10, 0.4, "Label/Music/Mute.png")
        print(self.GetVolume())

    def MusicTabVolumeDownDef(self):
        if (self.MusicVolume > 0):
            self.MusicVolume -= 0.01
        self.SetVolume(self.MusicVolume)
        if (self.MusicVolume > 0.06):
            self.ChangeImageFading(self.MusicTabVolume, 11, 0.4, "Label/Music/High.png")
        elif (self.MusicVolume > 0.03):
            self.ChangeImageFading(self.MusicTabVolume, 12, 0.4, "Label/Music/Medium.png")
        elif (self.MusicVolume > 0):
            self.ChangeImageFading(self.MusicTabVolume, 13, 0.4, "Label/Music/Low.png")
        else:
            self.ChangeImageFading(self.MusicTabVolume, 14, 0.4, "Label/Music/Mute.png")
        print(self.GetVolume())

    def MenuActive(self):
        print("pressed")
        opacity = QGraphicsOpacityEffect(self)
        opacity.setOpacity(0)
        self.MenuWidget.setGraphicsEffect(opacity)
        self.MenuWidgetAnim = QPropertyAnimation(opacity, b"opacity")
        self.MenuWidgetAnim.setDuration(250)
        self.MenuWidgetAnim.setStartValue(0)
        self.MenuWidgetAnim.setEndValue(1)
        self.MenuWidgetAnim.start()
        opacity = QGraphicsOpacityEffect(self)
        self.MenuButton.setGraphicsEffect(opacity)
        self.MenuButtonAnim = QPropertyAnimation(opacity, b"opacity")
        self.MenuButtonAnim.setDuration(250)
        self.MenuButtonAnim.setStartValue(0.7)
        self.MenuButtonAnim.setEndValue(0.4)
        self.MenuButtonAnim.start()
        blurBG = QGraphicsBlurEffect(self)
        blurBG.setBlurRadius(0)
        self.BGLabel1.setGraphicsEffect(blurBG)
        self.BGLabeAnim = QPropertyAnimation(blurBG, "blurRadius")
        self.BGLabeAnim.setDuration(250)
        self.BGLabeAnim.setStartValue(0)
        self.BGLabeAnim.setEndValue(10)
        self.BGLabeAnim.start()

    def MenuRoomBTNDef(self):
        self.RoomBTN.click()
        self.HomeState = "Room"
        self.FadeUpFadeDown(self.MenuRoomBTN, 18, 0.7, 0.15)

    def MenuTempBTNDef(self):
        self.TempCoBTN.click()
        self.HomeState = "TempCo"
        self.FadeUpFadeDown(self.MenuTempBTN, 19, 0.7, 0.15)

    def MenuBaleBTNDef(self):
        self.SocialBTN.click()
        self.HomeState = "Social"
        self.FadeUpFadeDown(self.MenuBaleBTN, 20, 0.7, 0.15)

    def MenuMusicBTNDef(self):
        self.MusicBTN.click()
        self.HomeState = "Music"
        self.FadeUpFadeDown(self.MenuMusicBTN, 21, 0.7, 0.15)

    def MenuSetBTNDef(self):
        self.SettingBTN.click()
        self.HomeState = "Setting"
        self.FadeUpFadeDown(self.MenuSetBTN, 22, 0.7, 0.15)

    def MenuRelease(self):
        self.MenuButtonY = int(self.MenuButton.geometry().y())
        if (self.MenuButtonY < 75):
            self.HomeBTN.click()
            self.HomeState = "Home"
        elif (self.MenuButtonY < 175):
            self.RoomBTN.click()
            self.HomeState = "Room"
        elif (self.MenuButtonY < 275):
            self.TempCoBTN.click()
            self.HomeState = "TempCo"
        elif (self.MenuButtonY < 375):
            self.MusicBTN.click()
            self.HomeState = "Music"
        elif (self.MenuButtonY < 475):
            self.SocialBTN.click()
            self.HomeState = "Social"
        elif (self.MenuButtonY < 575):
            self.SettingBTN.click()
            self.HomeState = "Setting"
        opacity = QGraphicsOpacityEffect(self)
        opacity.setOpacity(1)
        self.MenuWidget.setGraphicsEffect(opacity)
        self.MenuWidgetAnim = QPropertyAnimation(opacity, b"opacity")
        self.MenuWidgetAnim.setDuration(250)
        self.MenuWidgetAnim.setStartValue(1)
        self.MenuWidgetAnim.setEndValue(0)
        self.MenuWidgetAnim.start()
        opacity = QGraphicsOpacityEffect(self)
        self.MenuButton.setGraphicsEffect(opacity)
        self.MenuButtonAnim = QPropertyAnimation(opacity, b"opacity")
        self.MenuButtonAnim.setDuration(250)
        self.MenuButtonAnim.setStartValue(0.4)
        self.MenuButtonAnim.setEndValue(0.7)
        self.MenuButtonAnim.start()
        blurBG = QGraphicsBlurEffect(self)
        blurBG.setBlurRadius(10)
        self.BGLabel1.setGraphicsEffect(blurBG)
        self.BGLabeAnim = QPropertyAnimation(blurBG, "blurRadius")
        self.BGLabeAnim.setDuration(250)
        self.BGLabeAnim.setStartValue(10)
        self.BGLabeAnim.setEndValue(0)
        self.BGLabeAnim.start()

        self.MenuButtonGAnim = QPropertyAnimation(self.MenuButton, b"geometry")
        self.MenuButtonGAnim.setDuration(250)
        # self.MenuButtonGAnim.setStartValue(QRect(2, 30, 100, 100))
        self.MenuButtonGAnim.setEndValue(2, -2, 100, 100)
        self.MenuButtonGAnim.start()

    def FadeUnfade(self, Widget, NumOfBTN):
        if (self.FadeUnfadeAnim[NumOfBTN] != 0):
            self.FadeUnfadeAnim[NumOfBTN].deleteLater()
        self.effect = QGraphicsOpacityEffect()
        Widget.setGraphicsEffect(self.effect)
        self.FadeUnfadeAnim[NumOfBTN] = QPropertyAnimation(self.effect, b"opacity")
        self.FadeUnfadeAnim[NumOfBTN].setDuration(500)
        self.FadeUnfadeAnim[NumOfBTN].setKeyValueAt(0, 0.4)
        self.FadeUnfadeAnim[NumOfBTN].setKeyValueAt(0.5, 0)
        self.FadeUnfadeAnim[NumOfBTN].setKeyValueAt(1, 0.4)
        self.FadeUnfadeAnim[NumOfBTN].start()

    def FadeUpFadeDown(self, Widget, NumOfBTN, opacity, opacityHigh):
        if (self.FadeUpFadeDownAnim[NumOfBTN] != 0):
            self.FadeUpFadeDownAnim[NumOfBTN].deleteLater()
        self.effect = QGraphicsOpacityEffect()
        Widget.setGraphicsEffect(self.effect)
        self.FadeUpFadeDownAnim[NumOfBTN] = QPropertyAnimation(self.effect, b"opacity")
        self.FadeUpFadeDownAnim[NumOfBTN].setDuration(350)
        self.FadeUpFadeDownAnim[NumOfBTN].setKeyValueAt(0, opacity)
        self.FadeUpFadeDownAnim[NumOfBTN].setKeyValueAt(0.25, (2*opacity+opacityHigh)/3)
        self.FadeUpFadeDownAnim[NumOfBTN].setKeyValueAt(0.5, opacityHigh)
        self.FadeUpFadeDownAnim[NumOfBTN].setKeyValueAt(0.75, (2*opacity+opacityHigh)/3)
        self.FadeUpFadeDownAnim[NumOfBTN].setKeyValueAt(1, opacity)
        self.FadeUpFadeDownAnim[NumOfBTN].start()

    def FadeTimerHomeDef(self, Widget, NumOfBTN, opacity, opacityHigh):
        if (self.FadeTimerHome[NumOfBTN] != 0):
            self.FadeTimerHome[NumOfBTN].deleteLater()
        self.effect = QGraphicsOpacityEffect()
        Widget.setGraphicsEffect(self.effect)
        self.FadeTimerHome[NumOfBTN] = QPropertyAnimation(self.effect, b"opacity")
        self.FadeTimerHome[NumOfBTN].setDuration(2000)
        self.FadeTimerHome[NumOfBTN].setKeyValueAt(0, opacity)
        self.FadeTimerHome[NumOfBTN].setKeyValueAt(0.5, opacityHigh)
        self.FadeTimerHome[NumOfBTN].setKeyValueAt(1, opacity)
        self.FadeTimerHome[NumOfBTN].start()

    def FadeOutIn(self, Widget, NumOfBTN, Fopacity, Sopacity):
        if (self.FadeIO[NumOfBTN] != 0):
            self.FadeIO[NumOfBTN].deleteLater()
        self.effect = QGraphicsOpacityEffect()
        Widget.setGraphicsEffect(self.effect)
        self.FadeIO[NumOfBTN] = QPropertyAnimation(self.effect, b"opacity")
        self.FadeIO[NumOfBTN].setDuration(500)
        self.FadeIO[NumOfBTN].setKeyValueAt(0, Fopacity)
        self.FadeIO[NumOfBTN].setKeyValueAt(1, Sopacity)
        self.FadeIO[NumOfBTN].start()

    def ChangeImageFading(self, Widget, NumOfBTN, opacity1, Image):
        if (self.ChangeImageFadeGroup[NumOfBTN] != 0):
            self.ChangeImageFadeGroup[NumOfBTN].deleteLater()
        if (self.ChangeImageFade[NumOfBTN] != 0):
            self.ChangeImageFade[NumOfBTN].deleteLater()
        self.ChangeImageFadeGroup[NumOfBTN] = QSequentialAnimationGroup()
        self.effect1 = QGraphicsOpacityEffect()
        Widget.setGraphicsEffect(self.effect1)
        self.ChangeImageFade[NumOfBTN] = QPropertyAnimation(self.effect1, b"opacity")
        self.ChangeImageFade[NumOfBTN].setDuration(250)
        self.ChangeImageFade[NumOfBTN].setKeyValueAt(0, opacity1)
        self.ChangeImageFade[NumOfBTN].setKeyValueAt(1, 0)
        self.ChangeImageFade[NumOfBTN].finished.connect(lambda: self.ChangeImage(Widget, Image))
        self.ChangeImageFadeGroup[NumOfBTN].addAnimation(self.ChangeImageFade[NumOfBTN])
        Widget.setGraphicsEffect(self.effect1)
        self.ChangeImageFade[NumOfBTN] = QPropertyAnimation(self.effect1, b"opacity")
        self.ChangeImageFade[NumOfBTN].setDuration(250)
        self.ChangeImageFade[NumOfBTN].setKeyValueAt(0, 0)
        self.ChangeImageFade[NumOfBTN].setKeyValueAt(1, opacity1)
        self.ChangeImageFadeGroup[NumOfBTN].addAnimation(self.ChangeImageFade[NumOfBTN])
        self.ChangeImageFadeGroup[NumOfBTN].start()

    def ChangeImage(self, widget, Image):
        widget.setIcon(QIcon(Image))

    def PlayMusic(self, MusicPath):
        pygame.init()
        pygame.mixer.music.fadeout
        pygame.mixer.music.load(MusicPath)
        pygame.mixer.music.play()

    def IsPlaying(self):
        pygame.init()
        return pygame.mixer.music.get_busy()

    def GetPosOfMusic(self):
        pygame.init()
        return pygame.mixer.music.get_pos()

    def GetVolume(self):
        pygame.init()
        return pygame.mixer.music.get_volume()

    def SetPosOfMusic(self, Pos):
        pygame.init()
        return pygame.mixer.music.set_pos(Pos)

    def SetVolume(self, Volume):
        pygame.init()
        return pygame.mixer.music.set_volume(Volume)

    def PauseMusic(self):
        pygame.init()
        return pygame.mixer.music.pause()

    def UnpauseMusic(self):
        pygame.init()
        return pygame.mixer.music.unpause()

    def SecurityDef(self):
        if (self.securityBool == True): # ! and  int(GPIO.input(16)) == 1):
            if (self.securityCount == 0):
                self.bot.sendMessage(MAJN_ID, "Someone is in your room...")
                # ! camera = PiCamera()
                # ! time.sleep(2)
                # ! camera.capture("img.png")
                # ! del camera
                bot.sendMessage(MAJN_ID, 'Photo has taken, Sending...')
                try:
                    bot.send_photo(MAJN_ID, photo=open('img.png', 'rb'),caption= "❗ Someone is in your Room ❗")
                except:
                    pass
                bot.sendMessage(MAJN_ID, 'Done')
            self.securityCount = self.securityCount + 1
            if (self.securityCount == 10):
                self.securityCount = 0