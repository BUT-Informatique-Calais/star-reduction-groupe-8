import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ViewsResults(QWidget):
    def __init__(self, info: str):
        super().__init__()

        # Window settings
        self.resize(1000, 500)

        # Global style
        self.setStyleSheet("""
            QWidget {
                background-color: #FAF7F2;
            }

            QLabel {
                color: #2C2C2C;
            }

            QPushButton {
                background-color: #6EC1E4;
                color: white;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #5AB0D6;
            }

            QPushButton:pressed {
                background-color: #4AA0C6;
            }
        """)

        # Main layout
        self.MainLayout = QVBoxLayout()
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setSpacing(0)

        # Layout of the main informations
        self.LayoutActions = QVBoxLayout()
        self.title = QLabel("SAE Astronomy")
        self.title_font = QFont("Segoe UI", 46, QFont.Weight.Bold)
        self.title.setFont(self.title_font)
        self.LayoutActions.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Layout of the picture (results)
        self.LayoutPicture = QHBoxLayout()

        # Layout of the informations
        self.LayoutInformation = QVBoxLayout()
        self.exit = QPushButton("self.exit")
        self.exit.setFixedSize(100,20)
        informations = QLabel(info)
        informations_font = QFont("Segoe UI", 15)
        informations.setFont(informations_font)
        self.LayoutInformation.addWidget(informations, alignment=Qt.AlignmentFlag.AlignCenter)
        self.LayoutInformation.addWidget(self.exit, alignment=Qt.AlignmentFlag.AlignCenter)

        # Assembly
        self.MainLayout.addLayout(self.LayoutActions, 3)
        self.MainLayout.addLayout(self.LayoutPicture,3)
        self.MainLayout.addLayout(self.LayoutInformation, 1)
        self.setLayout(self.MainLayout)


# Tests
if __name__ == "__main__":
    app = QApplication(sys.argv)
    message = "Armand Cuvelier - Nolan Vannorenberghe - Jordan Sow - Version 1 - developed on 09/01/2026"
    views = ViewsResults(message)
    views.show()
    sys.self.exit(app.exec())