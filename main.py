from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QApplication, QTableWidgetItem, QDialog
import sqlite3


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.table = self.tableWidget

        table = self.table
        table.setColumnCount(7)
        table.setRowCount(1)  # change later

        table.setHorizontalHeaderLabels(["ID", "sort", "roasting", "in grains", "taste", "price", "size"])
        self.button.clicked.connect(self.open_form)
        self.show_table()

    def show_table(self):
        table = self.table
        # table.setColumnCount(7)
        # table.setRowCount(1)  # change later
        #
        # table.setHorizontalHeaderLabels(["ID", "sort", "roasting", "in grains", "taste", "price", "size"])

        with sqlite3.connect('coffee.db') as con:
            cur = con.cursor()

            result = list(cur.execute(f"""SELECT * FROM coffee"""))
            print(result)

        table.setRowCount(len(result))

        for row in range(len(result)):
            for col in range(7):
                table.setItem(row, col, QTableWidgetItem(str(result[row][col])))

        table.resizeColumnsToContents()

    def open_form(self):
        form = SecondWindow(self)
        print(form)
        # while not form.exec_():
        #     pass
        # print(form.exec_())
        if form.exec_():
            # form.close()
            print('here')
            # print(form.get_values())
            print('complted')
            sort, roasting, in_grains, taste, price, size = form.get_values()
            print('here')
            with sqlite3.connect('coffee.db') as con:
                cur = con.cursor()

                cur.execute(f"""INSERT INTO coffee(sort, roasting, in_grains, taste, price, size) 
    VALUES("{sort}", "{roasting}", "{in_grains}", "{taste}", {price}, {size})""")
            print('done')
            self.show_table()


class SecondWindow(QDialog):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.comboBox.addItems(['молотый', 'в зернах'])
        # self.ok_button.clicked.connect(self.got_close_signal)
        # self.cancel_button.clicked.connect(self.got_close_signal)
        self.show()
        self.ok_pressed = None

    def get_values(self):
        print('1')
        self.sort = self.lineEdit.text()
        print('2')
        self.roasting = self.lineEdit_2.text()
        self.in_grains = self.comboBox.currentText()
        self.taste = self.lineEdit_3.text()

        self.price = self.spinBox.value()
        print('3')
        self.size_local = self.spinBox_2.value()
        return self.sort, self.roasting, self.in_grains, self.taste, self.price, self.size_local

    def got_close_signal(self):
        print('close')
        if self.sender() == self.ok_button:
            self.ok_pressed = True
        else:
            self.ok_pressed = False
        self.hide()
        self.exec()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mw = Example()
    mw.show()
    sys.exit(app.exec())