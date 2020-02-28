#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import webapp
import webbrowser
from threading import Timer
import time
import types
import sys
import os
from collections import OrderedDict
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QTextBrowser, QCheckBox, QGridLayout, QSpacerItem, QSizePolicy, QSystemTrayIcon, QStyle, QAction, QMenu, qApp, QWidget, QLabel
from PySide2.QtCore import QFile, QObject
from PySide2 import QtWidgets, QtCore, QtGui
import threading
from multiprocessing import Process

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_path)


class Form(QObject):
    """
            Объявление чекбокса и иконки системного трея.
            Инициализироваться будут в конструкторе.
        """
    check_box = None
    tray_icon = None

    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)

        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.window.setWindowTitle("E-CONNECTOR")  # Устанавливаем заголовок окна
        self.check_box = self.window.findChild(QCheckBox, 'checkBox')

        btn = self.window.findChild(QPushButton, 'pushButton')
        btn.clicked.connect(self.ok_handler)

        # Инициализируем QSystemTrayIcon
        self.window.tray_icon = QSystemTrayIcon(self.window)
        self.window.tray_icon.setIcon(self.window.style().standardIcon(QStyle.SP_ComputerIcon))

        '''
                    Объявим и добавим действия для работы с иконкой системного трея
                    show - показать окно
                    hide - скрыть окно
                    exit - выход из программы
                '''
        show_action = QAction("Show", self.window)
        quit_action = QAction("Exit", self.window)
        hide_action = QAction("Hide", self.window)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.window.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.window.tray_icon.setContextMenu(tray_menu)
        self.window.tray_icon.show()
        # self.window.installEventFilter(self)

    # Переопределение метода closeEvent, для перехвата события закрытия окна
    # Окно будет закрываться только в том случае, если нет галочки в чекбоксе
    # def eventFilter(self, obj, event):
    #     if self.check_box.isChecked() and obj is self.window:
    #         event.ignore()
    #         self.window.hide()
    #         self.window.tray_icon.showMessage(
    #             "Tray Program",
    #             "Application was minimized to Tray",
    #             QSystemTrayIcon.Information,
    #             2000
    #         )
    #     if obj is self.window and event.type() == QtCore.QEvent.Close:
    #         self.quit_app()
    #         event.ignore()
    #         return True
    #     return super(Form, self).eventFilter(obj, event)


    # @QtCore.Slot()
    # def quit_app(self):
    #     # some actions to perform before actually quitting:
    #     print('CLEAN EXIT')
    #     self.window.removeEventFilter(self)
    #     app.quit()

    def ok_handler(self):
        self.window.hide()
        self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.Tool)
        self.window.tray_icon.show()
        # self.window.tray_icon.showMessage(
        #             "Tray Program",
        #             "Application was minimized to Tray",
        #             QSystemTrayIcon.Information,
        #             2000
        #         )
        self.open_browser()
        # self.flask_run()
        # t2 = threading.Thread(target=self.flask_run()).start()
        # t2.join()

        # p2 = Process(target=self.flask_run()).start()
        # p2.join()

    def flask_run(self):
        appflask = webapp.create_app()
        appflask.run()


    def show(self):
        self.window.show()


    def open_browser(self):
        webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_path = resource_path("mainwindow.ui")
    form = Form(file_path)
    # form.show()
    # p1 = Process(target=form.show()).start()
    # p1.join()

    t1  = threading.Thread(target=form.show()).start()

    appflask = webapp.create_app()
    t2 = Process(target=appflask.run()).start()
    t2.join()

    t1 .join()

    sys.exit(app.exec_())



