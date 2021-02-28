from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog, QInputDialog, \
    QDialogButtonBox, QLabel
import sqlite3
from main_ui import Ui_MainWindow
from addEditCoffeeForm_ui import Ui_Dialog


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.setupUi(self)
        # uic.loadUi('main.ui', self)
        # self.table = self.tableWidget

        table = self.tableWidget
        table.setColumnCount(7)
        table.setRowCount(1)  # change later

        table.setHorizontalHeaderLabels(["ID", "sort", "roasting", "in grains", "taste", "price", "size"])
        self.button.clicked.connect(self.open_form)
        self.button2.clicked.connect(self.edit_form)
        self.button3.clicked.connect(self.delete_form)
        self.show_table()

    def show_table(self):
        table = self.tableWidget
        # table.setColumnCount(7)
        # table.setRowCount(1)  # change later
        #
        # table.setHorizontalHeaderLabels(["ID", "sort", "roasting", "in grains", "taste", "price", "size"])

        with sqlite3.connect('data/coffee.db') as con:
            cur = con.cursor()

            result = list(cur.execute(f"""SELECT * FROM coffee"""))
            # print(result)

        table.setRowCount(len(result))

        for row in range(len(result)):
            for col in range(7):
                table.setItem(row, col, QTableWidgetItem(str(result[row][col])))

        table.resizeColumnsToContents()

    def open_form(self):
        form = SecondWindow(self)
        # print(form)
        # while not form.exec_():
        #     pass
        # # print(form.exec_())
        if form.exec_():
            # form.close()
            # print('here')
            # # print(form.get_values())
            # print('complted')
            sort, roasting, in_grains, taste, price, size = form.get_values()
            # print('here')
            with sqlite3.connect('data/coffee.db') as con:
                cur = con.cursor()

                cur.execute(f"""INSERT INTO coffee(sort, roasting, in_grains, taste, price, size) 
    VALUES("{sort}", "{roasting}", "{in_grains}", "{taste}", {price}, {size})""")
            # print('done')
            self.show_table()

    def edit_form(self):
        form = ThirdWindow(self)
        if form.exec_():
            sort, roasting, in_grains, taste, price, size = form.get_values()
            id = form.get_id()
            with sqlite3.connect('data/coffee.db') as con:
                cur = con.cursor()

                cur.execute(f"""UPDATE coffee
SET sort = "{sort}", roasting = "{roasting}", in_grains = "{in_grains}", 
taste = "{taste}", price = {price}, size = {size} 
WHERE id = {id}""")
                con.commit()
            self.show_table()

    def delete_form(self):
        form = FourthWindow(self)
        if form.exec_():
            id = form.return_id()
            # print(id, 'here')
            with sqlite3.connect('data/coffee.db') as con:
                cur = con.cursor()

                cur.execute(f"""DELETE FROM coffee
WHERE ID = {id}""")
                con.commit()
                # print('successfully')
            self.show_table()


class SecondWindow(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.setupUi(self)
        # uic.loadUi('addEditCoffeeForm.ui', self)
        self.comboBox.addItems(['молотый', 'в зернах'])
        # self.ok_button.clicked.connect(self.got_close_signal)
        # self.cancel_button.clicked.connect(self.got_close_signal)
        self.show()
        self.ok_pressed = None

    def get_values(self):
        # print('1')
        self.sort = self.lineEdit.text()
        # print('2')
        self.roasting = self.lineEdit_2.text()
        self.in_grains = self.comboBox.currentText()
        self.taste = self.lineEdit_3.text()

        self.price = self.spinBox.value()
        # print('3')
        self.size_local = self.spinBox_2.value()
        return self.sort, self.roasting, self.in_grains, self.taste, self.price, self.size_local

    # def got_close_signal(self):
    #     # print('close')
    #     if self.sender() == self.ok_button:
    #         self.ok_pressed = True
    #     else:
    #         self.ok_pressed = False
    #     self.hide()
    #     self.exec()


class ThirdWindow(SecondWindow):
    def __init__(self, parent=None):
        super(ThirdWindow, self).__init__(parent)
        self.hide()
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Введите id строки, которую хотите изменить: ')
        if ok:
            self.id = text
            # print('here')
            with sqlite3.connect('data/coffee.db') as con:
                cur = con.cursor()

                result = list(cur.execute(f"""SELECT sort, roasting, in_grains, taste, price, size 
FROM coffee
WHERE ID = {text}"""))[0]
            # print('1')
            self.lineEdit.setText(result[0])
            self.lineEdit_2.setText(result[1])
            # print('2')
            # print(self.comboBox)
            index = self.comboBox.findText(result[2], QtCore.Qt.MatchFixedString)
            self.comboBox.setCurrentIndex(index)
            # print('3')
            self.lineEdit_3.setText(result[3])
            self.spinBox.setValue(result[4])
            # print('4')
            self.spinBox_2.setValue(result[5])
            # print('5')
            self.show()

    def get_id(self):
        return self.id


class FourthWindow(QDialog):
    def __init__(self, parent=None):
        super(FourthWindow, self).__init__(parent)
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Введите id строки, которую хотите удалить: ')
        if ok:
            self.id = text
            # print(self.id)
            # self.resize(200, 50)
            self.setFixedSize(200, 50)
            butonbox = QDialogButtonBox(self)
            # print('here')
            ok = butonbox.addButton(QDialogButtonBox.Ok)
            cancel = butonbox.addButton(QDialogButtonBox.Cancel)
            # print('here2')
            ok.clicked.connect(self.accepted)
            cancel.clicked.connect(self.rejected)
            butonbox.setGeometry(0, 25, 200, 25)
            with sqlite3.connect('data/coffee.db') as con:
                cur = con.cursor()

                result = list(cur.execute(f"""SELECT sort, roasting, in_grains, taste, price, size 
FROM coffee
WHERE id = {text}"""))[0]
                # print(result)
            self.label = QLabel(f'''Вы собираетесь удалить строку:
{", ".join([str(x) for x in result])}''', self)
            self.show()

    def return_id(self):
        return self.id

    def accepted(self) -> None:
        super(FourthWindow, self).accept()

    def rejected(self) -> None:
        super(FourthWindow, self).reject()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mw = Example()
    mw.show()
    sys.exit(app.exec())