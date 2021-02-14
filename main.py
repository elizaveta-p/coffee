from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QApplication, QTableWidgetItem
import sqlite3


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.table = self.tableWidget
        self.show_table()

    def show_table(self):
        table = self.table
        table.setColumnCount(7)
        table.setRowCount(1)  # change later

        table.setHorizontalHeaderLabels(["ID", "sort", "roasting", "in grains", "taste", "price", "size"])

        with sqlite3.connect('coffee.db') as con:
            cur = con.cursor()

            result = list(cur.execute(f"""SELECT * FROM coffee"""))
            print(result)

        for row in range(len(result)):
            for col in range(7):
                table.setItem(row, col, QTableWidgetItem(str(result[row][col])))

        table.resizeColumnsToContents()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mw = Example()
    mw.show()
    sys.exit(app.exec())