from PyQt5.QtWidgets import QTableView, QMessageBox
from PyQt5.QtCore import pyqtSlot
import psycopg2
import settings as st
import db

from .Model import Model
from .Dialog import Dialog


SELECT_ONE = '''
    SELECT AirlineID, Model, Capacity
    FROM Plane
    WHERE PlaneID = %s;
'''


class View(QTableView):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        model = Model(parent=self)
        self.setModel(model)
        
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)
        
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)
        
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
    
    @property
    def planeid(self):
        row = self.currentIndex().row()
        return self.model().record(row).value(0)
    
    @pyqtSlot()
    def add(self):
        dia = Dialog(parent=self)
        if dia.exec():
            data = db.Plane()
            dia.get(data)
            data.save()
            self.model().fresh()
    
    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        data = db.Plane(planeid=self.planeid).load()
        dia.put(data)
        if dia.exec():
            dia.get(data)
            data.save()
            self.model().fresh()
    
    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_plane = self.model().record(row).value(0)
        ans = QMessageBox.question(self, 'Самолет', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().delete(id_plane)
