#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import threading
import webbrowser

from PySide2 import QtCore
from PySide2.QtCore import QFile, QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QCheckBox, QSystemTrayIcon, QStyle, QAction, QMenu, qApp

import webapp


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

        appflask = webapp.create_app()
        thread = threading.Thread(target=appflask.run).start()

        # Инициализируем QSystemTrayIcon
        self.window.tray_icon = QSystemTrayIcon(self.window)
        self.window.tray_icon.setIcon(self.window.style().standardIcon(QStyle.SP_ComputerIcon))

        '''
                    Объявим и добавим действия для работы с иконкой системного трея
                    show - показать окно
                    hide - скрыть окно
                    exit - выход из программы
                '''
        show_action = QAction("Показать окно", self.window)
        quit_action = QAction("Выход из программы", self.window)
        hide_action = QAction("Свернуть окно", self.window)
        show_action.triggered.connect(self.window.show)
        hide_action.triggered.connect(self.window.hide)
        quit_action.triggered.connect(self.quit_app)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.window.tray_icon.setContextMenu(tray_menu)
        self.window.tray_icon.show()
        self.window.installEventFilter(self)

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
    def quit_app(self):
         webbrowser.open_new('http://127.0.0.1:5000/shutdown')
         # some actions to perform before actually quitting:
         self.window.removeEventFilter(self)
         self.window.close()
         print('CLEAN EXIT')
         app.quit()

    def ok_handler(self):
        self.window.hide()
        self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.Tool)
        self.window.tray_icon.showMessage(
                    "Tray Program",
                    "Application was minimized to Tray",
                    QSystemTrayIcon.Information,
                    2000
                )
        webbrowser.open_new('http://127.0.0.1:5000/')


    def show(self):
        self.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_path = resource_path("mainwindow.ui")
    form = Form(file_path)
    form.show()
    sys.exit(app.exec_())



