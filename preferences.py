# -*- coding: utf-8 -*-

from typing import Optional, Union

import pyqtgraph as pg  # type: ignore
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QGroupBox, \
    QSpinBox, QVBoxLayout, QWidget

from colorselector import ColorSelector
from settings import Settings

__all__ = ['Preferences']


class Preferences(QDialog):
    """ GUI preferences dialog """

    def __init__(self, settings: Settings, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.settings: Settings = settings
        self.setModal(True)
        self.setWindowTitle(self.tr('Preferences'))
        if parent is not None:
            self.setWindowIcon(parent.windowIcon())

        check_box: QCheckBox
        combo_box: QComboBox
        spin_box: pg.SpinBox
        q_spin_box: Union[QSpinBox, QDoubleSpinBox]
        color_selector: ColorSelector

        layout: QVBoxLayout = QVBoxLayout(self)
        for key, value in self.settings.dialog.items():
            if isinstance(value, dict) and value:
                box: QGroupBox = QGroupBox(key, self)
                box_layout: QFormLayout = QFormLayout(box)
                for key2, value2 in value.items():
                    if isinstance(value2, tuple) and isinstance(value2[-1], str) and value2[-1]:
                        if len(value2) == 1:
                            if isinstance(getattr(self.settings, value2[-1]), bool):
                                check_box = QCheckBox(self.tr(key2), box)
                                setattr(check_box, 'callback', value2[-1])
                                check_box.setChecked(getattr(self.settings, value2[-1]))
                                check_box.toggled.connect(
                                    lambda x: setattr(self.settings, getattr(self.sender(), 'callback'), x))
                                box_layout.addWidget(check_box)
                            elif isinstance(getattr(self.settings, value2[-1]), QColor):
                                color_selector = ColorSelector(box, getattr(self.settings, value2[-1]))
                                setattr(color_selector, 'callback', value2[-1])
                                color_selector.colorSelected.connect(
                                    lambda x: setattr(self.settings, getattr(self.sender(), 'callback'), x))
                                box_layout.addRow(key2, color_selector)
                            # no else
                        elif len(value2) == 2:
                            value3 = value2[0]
                            if isinstance(value3, (list, tuple)):
                                combo_box = QComboBox(box)
                                setattr(combo_box, 'callback', value2[-1])
                                for item in value3:
                                    combo_box.addItem(self.tr(item))
                                combo_box.setCurrentIndex(getattr(self.settings, value2[-1]))
                                combo_box.currentIndexChanged.connect(
                                    lambda x: setattr(self.settings, getattr(self.sender(), 'callback'), x))
                                box_layout.addRow(self.tr(key2), combo_box)
                            elif isinstance(getattr(self.settings, value2[-1]), float) and isinstance(value3, dict):
                                spin_box = pg.SpinBox(box, getattr(self.settings, value2[-1]))
                                spin_box.setOpts(**value3)
                                setattr(spin_box, 'callback', value2[-1])
                                spin_box.valueChanged.connect(
                                    lambda x: setattr(self.settings, getattr(self.sender(), 'callback'), x))
                                box_layout.addRow(key2, spin_box)
                            # no else
                        elif len(value2) == 3:
                            value3a = value2[0]
                            value3b = value2[1]
                            if isinstance(value3a, (list, tuple)) and isinstance(value3b, (list, tuple)):
                                combo_box = QComboBox(box)
                                setattr(combo_box, 'callback', value2[-1])
                                for index, item in enumerate(value3a):
                                    combo_box.addItem(self.tr(item), value3b[index])
                                combo_box.setCurrentIndex(value3b.index(getattr(self.settings, value2[-1])))
                                combo_box.currentIndexChanged.connect(
                                    lambda _: setattr(self.settings, getattr(self.sender(), 'callback'),
                                                      self.sender().currentData()))
                                box_layout.addRow(self.tr(key2), combo_box)
                            elif (isinstance(value3a, slice)
                                  and isinstance(getattr(self.settings, value2[-1]), (int, float))
                                  and isinstance(value3b, tuple)):
                                if ((value3a.start is None or isinstance(value3a.start, int))
                                        and (value3a.stop is None or isinstance(value3a.stop, int))
                                        and (value3a.step is None or isinstance(value3a.step, int))
                                        and isinstance(getattr(self.settings, value2[-1]), int)):
                                    q_spin_box = QSpinBox(box)
                                else:
                                    q_spin_box = QDoubleSpinBox(box)
                                setattr(q_spin_box, 'callback', value2[-1])
                                if value3a.start is not None:
                                    q_spin_box.setMinimum(value3a.start)
                                if value3a.stop is not None:
                                    q_spin_box.setMaximum(value3a.stop)
                                if value3a.step is not None:
                                    q_spin_box.setSingleStep(value3a.step)
                                q_spin_box.setValue(getattr(self.settings, value2[-1]))
                                if len(value3b) == 2:
                                    q_spin_box.setPrefix(str(value3b[0]))
                                    q_spin_box.setSuffix(str(value3b[1]))
                                elif len(value3b) == 1:
                                    q_spin_box.setSuffix(str(value3b[0]))
                                # no else
                                q_spin_box.valueChanged.connect(
                                    lambda _: setattr(self.settings, getattr(self.sender(), 'callback'),
                                                      self.sender().value()))
                                box_layout.addRow(self.tr(key2), q_spin_box)
                            # no else
                        # no else
                    # no else
                layout.addWidget(box)
            # no else
        buttons: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Close, self)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
