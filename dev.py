from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(5, 2, self)  # Create a table with 5 rows and 2 columns
        self.setCentralWidget(self.table)

        for i in range(5):  # For each row
            for j in range(2):  # For each column
                item = QTableWidgetItem(f"Item {i}-{j}")
                if j == 1:  # If the column number is 1
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)  # Make the item not selectable
                self.table.setItem(i, j, item)

        self.table.itemSelectionChanged.connect(self.print_selected_item)

    def print_selected_item(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            print(selected_items[0].text())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())