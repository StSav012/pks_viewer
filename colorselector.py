# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QColorDialog, QPushButton, QWidget

__all__ = ['ColorSelector']


class ColorSelector(QPushButton):
    colorSelected = pyqtSignal(QColor, name='colorSelected')

    def __init__(self, parent: QWidget, color: QColor) -> None:
        super().__init__(parent)

        self.color: QColor = color

        self.setAutoFillBackground(True)
        self.paint_button()

        self.setText(self.color.name())

        self.color_dialog: QColorDialog = QColorDialog(self)
        self.color_dialog.colorSelected.connect(self.on_color_changed)

        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self) -> None:
        self.color_dialog.setCurrentColor(self.color)
        self.color_dialog.exec()

    def on_color_changed(self, color: QColor) -> None:
        self.color = color
        self.setText(self.color.name())
        self.paint_button()
        self.colorSelected.emit(color)

    def paint_button(self) -> None:
        pal: QPalette = self.palette()
        pal.setColor(QPalette.Button, self.color)
        pal.setColor(QPalette.ButtonText, QColor('white' if self.color.lightnessF() < 0.5 else 'black'))
        self.setPalette(pal)
        self.update()
