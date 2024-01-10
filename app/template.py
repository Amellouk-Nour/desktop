from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PySide2.QtCore import Qt, QPoint, QRect
from PySide2.QtGui import QCursor, QPixmap, QIcon

class FramelessWindow(QMainWindow):
    def __init__(self):
        super(FramelessWindow, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setGeometry(100, 100, 1500, 700)
        self.setMinimumSize(650, 650)
        self.oldPos = None
        self.resizing = False
        
        # Icon Label
        self.iconLabel = QLabel(self)
        pixmap = QPixmap(r"C:\$Winkernel\formation python\mini_projet\app\Logo1.png")
        self.iconLabel.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio))
        self.iconLabel.setFixedSize(70, 50)
        self.iconLabel.setStyleSheet("background-color: #001111;padding-left: 20px;")
        
        
        # Tab Bar
        self.tabBar = QLabel("Interface Administrateur")
        self.tabBar.setStyleSheet("background-color: #001111; color: white; padding: 5px;")
        self.tabBar.setFixedHeight(50)  # Hauteur fixe pour la barre d'onglet
        
        # Boutons
        closeButton = QPushButton("X")
        closeButton.setFixedSize(50, 50)
        closeButton.setStyleSheet("QPushButton { background-color: #001111; color: white; font-weight: bold; border: none; } QPushButton:hover { background-color: red; }")
        closeButton.clicked.connect(self.close)
        
        minimizeButton = QPushButton("_")
        minimizeButton.setFixedSize(50, 50)
        minimizeButton.setStyleSheet("QPushButton { background-color: #001111; color: white; font-weight: bold; border: none; } QPushButton:hover { background-color: grey; }")
        minimizeButton.clicked.connect(self.showMinimized)
        
        resizeButton = QPushButton("[]")
        resizeButton.setFixedSize(50, 50)
        resizeButton.setStyleSheet("QPushButton { background-color: #001111; color: white; font-weight: bold; border: none; } QPushButton:hover { background-color: grey; }")
        resizeButton.clicked.connect(self.toggleMaximizeRestore)
        
        # Layout pour les boutons à aligner avec la barre d'onglet
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(minimizeButton, 0, Qt.AlignTop)
        buttonsLayout.addWidget(resizeButton, 0, Qt.AlignTop)
        buttonsLayout.addWidget(closeButton, 0, Qt.AlignTop)
        buttonsLayout.setContentsMargins(0, 0, 0, 0)  # Pas de marge pour les boutons
        buttonsLayout.setSpacing(0)  # Pas d'espacement entre les boutons

        # Un seul Layout pour la barre d'onglet
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(self.iconLabel)  # Ajoute l'icône
        tabLayout.addWidget(self.tabBar, 1)
        tabLayout.addLayout(buttonsLayout)  # Ajout des boutons au layout
        tabLayout.setContentsMargins(0, 0, 0, 0)
        tabLayout.setSpacing(0)

        # Layout principal
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addLayout(tabLayout)  # Ajout de la barre d'onglet au layout
        mainLayout.addStretch()

        # Configuration du widget central
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def mousePressEvent(self, event):
        
        self.oldPos = event.globalPos()
        self.resizing = True if self.isInResizeArea(event.pos()) else False
        super(FramelessWindow, self).enterEvent(event)
        
    def mouseMoveEvent(self, event):
        pos = event.pos()
        resizeBorder = 10
        

        # Vérifier les bords pour le redimensionnement
        top = 0 < pos.y() < resizeBorder
        bottom = self.height() - resizeBorder < pos.y() < self.height()
        left = 0 < pos.x() < resizeBorder
        right = self.width() - resizeBorder < pos.x() < self.width()

        # Changer la forme du curseur en fonction de la position
        if (top and left) or (bottom and right):
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif (top and right) or (bottom and left):
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif top or bottom:
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif left or right:
            self.setCursor(QCursor(Qt.SizeHorCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

        if event.buttons() == Qt.LeftButton:
            if self.resizing:
                self.resizeWindow(event.globalPos())
                 
            elif self.tabBar.rect().contains(event.pos()):
                self.moveWindow(event.globalPos())

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.oldPos = None
        self.setCursor(QCursor(Qt.ArrowCursor))
    
    def toggleMaximizeRestore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    # def moveWindow(self, globalPos):
    #     if not self.resizing:
    #         delta = globalPos - self.oldPos
    #         self.move(self.x() + delta.x(), self.y() + delta.y())
    #         self.oldPos = globalPos
    def moveWindow(self, globalPos):
        if self.oldPos is None:
            self.oldPos = globalPos
        delta = globalPos - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = globalPos
    def isInResizeArea(self, pos):
        resizeBorder = 10
        top = 0 < pos.y() < resizeBorder
        bottom = self.height() - resizeBorder < pos.y() < self.height()
        left = 0 < pos.x() < resizeBorder
        right = self.width() - resizeBorder < pos.x() < self.width()

        self.resizeDirection = {
            'top': top, 'bottom': bottom, 'left': left, 'right': right
        }

        return top or bottom or left or right

    def resizeWindow(self, globalPos):
        delta = globalPos - self.oldPos
        self.oldPos = globalPos

        newGeometry = QRect(self.geometry())

        if self.resizeDirection['top']:
            newGeometry.setTop(newGeometry.top() + delta.y())
        if self.resizeDirection['bottom']:
            newGeometry.setBottom(newGeometry.bottom() + delta.y())
        if self.resizeDirection['left']:
            newGeometry.setLeft(newGeometry.left() + delta.x())
        if self.resizeDirection['right']:
            newGeometry.setRight(newGeometry.right() + delta.x())

        self.setGeometry(newGeometry)
if __name__ == "__main__":
    app = QApplication([])
    window = FramelessWindow()
    window.show()
    app.exec_()
