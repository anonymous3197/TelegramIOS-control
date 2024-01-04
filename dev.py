import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Get Values from QTableWidget')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(3)  # Số cột là 3 để minh họa
        layout.addWidget(self.tableWidget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def getValuesFromTable(self, row, column):
        if row < 0 or row >= self.tableWidget.rowCount() or column < 0 or column >= self.tableWidget.columnCount():
            return None

        item = self.tableWidget.item(row, column)
        if item is not None:
            return item.text()
        else:
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    # Đặt giá trị vào các ô trong bảng
    for row in range(3):
        for column in range(3):
            item = QTableWidgetItem(f'Value {row}-{column}')
            window.tableWidget.setItem(row, column, item)

    # Lấy giá trị từ ô ở hàng 1, cột 2 (index 0-based)
    row_index = 1
    col_index = 2
    value = window.getValuesFromTable(row_index, col_index)
    if value is not None:
        print(f'Value at row {row_index}, column {col_index}: {value}')

    sys.exit(app.exec_())
