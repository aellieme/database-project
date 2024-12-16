from PyQt5.QtWidgets import QTableView, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QFont
import db

from .Model import Model
from .Dialog import Dialog


class View(QTableView):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        model = Model(parent=self)
        title = QApplication.translate('Airlines.View', 'ID')
        model.setHeaderData(0, Qt.Horizontal, title)
        title = QApplication.translate('Airline.View', 'Airline Name')
        model.setHeaderData(1, Qt.Horizontal, title)
        title = QApplication.translate('Airline.View', 'IATA Code')
        model.setHeaderData(2, Qt.Horizontal, title)
        self.setModel(model)
        
        font = QFont()
        font.setPointSize(20)
        self.setFont(font)
             
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setWordWrap(False)
        
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        vh.setVisible(False)
        self.setVerticalHeader(vh)
        
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setStyleSheet("QHeaderView { font-size: 20pt; }") 
    
    @property
    def airlineid(self):
        row = self.currentIndex().row()
        return self.model().record(row).value(0)
    
    @pyqtSlot()
    def add(self):
        dia = Dialog(parent=self)
        if dia.exec():
            data = db.Airline()
            dia.get(data)
            data.save()
            self.model().fresh()
    
    @pyqtSlot()
    def update(self):
        if self.airlineid:
            dia = Dialog(parent=self)
            data = db.Airline(airlineid=self.airlineid).load()
            dia.put(data)
            if dia.exec():
                dia.get(data)
                data.save()
                self.model().fresh()
        else:
            QMessageBox.warning(self, 'Авиакомпания', 'Сначала выберете нужную авиакомпанию')
    
    @pyqtSlot()
    def delete(self):
        if self.airlineid:
            title = QApplication.translate('Airlines.View', 'Airline')
            q = QApplication.translate('Airlines.View', 'Are you sure?')
            ans = QMessageBox.question(self, title, q)
            if ans == QMessageBox.Yes:
                db.Airline(airlineid=self.airlineid).delete()
                self.model().fresh()
        else:
            QMessageBox.warning(self, 'Авиакомпания', 'Сначала выберете нужную авиакомпанию')
    
    @pyqtSlot()
    def truncate(self):
        title = QApplication.translate('Airlines.View', 'Airline')
        q = QApplication.translate('Airlines.View', 'Are you sure?')
        ans = QMessageBox.question(self, title, q)
        if ans == QMessageBox.Yes:
            db.Airline().truncate()
            self.model().fresh()
