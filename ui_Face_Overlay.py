# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Face_OverlaycEVqZI.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(660, 535)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 640, 500))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 10, 480, 480))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2.setLineWidth(0)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 480, 480))
        self.label.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(500, 10, 128, 480))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_3.setLineWidth(0)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 38, 128, 128))
        self.label_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 185, 108, 18))
        self.saveButton = QPushButton(self.frame_3)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setGeometry(QRect(10, 430, 100, 26))
        self.lineEdit = QLineEdit(self.frame_3)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(0, 210, 108, 26))
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 10, 108, 18))
        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 250, 66, 18))
        self.lineEdit_2 = QLineEdit(self.frame_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(0, 275, 113, 26))
        self.upButton = QPushButton(self.frame_3)
        self.upButton.setObjectName(u"upButton")
        self.upButton.setGeometry(QRect(32, 310, 60, 26))
        self.downButton = QPushButton(self.frame_3)
        self.downButton.setObjectName(u"downButton")
        self.downButton.setGeometry(QRect(32, 370, 60, 26))
        self.leftButton = QPushButton(self.frame_3)
        self.leftButton.setObjectName(u"leftButton")
        self.leftButton.setGeometry(QRect(0, 340, 60, 26))
        self.rightButton = QPushButton(self.frame_3)
        self.rightButton.setObjectName(u"rightButton")
        self.rightButton.setGeometry(QRect(65, 340, 60, 26))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 660, 27))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.saveButton.clicked.connect(MainWindow.save_button_clicked)
        self.downButton.clicked.connect(MainWindow.down_button_clicked)
        self.rightButton.clicked.connect(MainWindow.right_button_clicked)
        self.leftButton.clicked.connect(MainWindow.left_button_clicked)
        self.upButton.clicked.connect(MainWindow.up_button_clicked)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc778\uc774\ub984(Name)", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\uc5bc\uad74(Face)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5\uc774\ub984", None))
        self.upButton.setText(QCoreApplication.translate("MainWindow", u"UP", None))
        self.downButton.setText(QCoreApplication.translate("MainWindow", u"DOWN", None))
        self.leftButton.setText(QCoreApplication.translate("MainWindow", u"LEFT", None))
        self.rightButton.setText(QCoreApplication.translate("MainWindow", u"RIGHT", None))
    # retranslateUi

