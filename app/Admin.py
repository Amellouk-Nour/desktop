from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QFrame, QLineEdit, QTableWidget, QTableWidgetItem
from PySide2.QtCore import Qt, QPoint, QRect, QSize
from PySide2.QtGui import QCursor, QPixmap, QIcon
from tinydb import TinyDB, Query
import re,json
from pprint import pprint

class AdminFeature():
    def __init__(self):
        self.db_path = "dataBase.json"
        self.Utilisateurs = TinyDB(self.db_path).table("Users")
        self.User = Query()

    def sauvegarder_avec_indentation(self):
        with open(self.db_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            file.seek(0)
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.truncate()

    def ajouter_Prof(self, username, password, matiere):
        self.Utilisateurs.insert({
            "username": username,
            "password": password,
            "email": None,
            "permission": 1,
            "Matiere": matiere
        })
        self.sauvegarder_avec_indentation()

    def ajouter_Etudiant(self, username, password):
        self.Utilisateurs.insert({
            "username": username,
            "password": password,
            "email": None,
            "permission": 2,
            "Matiere": None
        })
        self.sauvegarder_avec_indentation()

    def return_all_users(self):
        return self.Utilisateurs.all()

    def search_user(self, debut_nom):
        if not debut_nom:
            search_results = self.return_all_users()
        else:
            search_results = self.Utilisateurs.search(self.User.username.search(debut_nom, flags=re.IGNORECASE))
        
        # Filtrer les utilisateurs dont l'id est 1 et ajouter 'doc_id' aux autres
        filtered_results = []
        for user in search_results:
            user['id'] = user.doc_id  # Ajoutez cette ligne si vous souhaitez que l'id soit explicitement dans le dictionnaire
            if user.doc_id != 1:  # Exclure l'utilisateur avec 'doc_id' égal à 1
                filtered_results.append(user)

        return filtered_results
    



class WelcomeWidget(QWidget):
    def __init__(self):
        super(WelcomeWidget, self).__init__()
        self.initUI()
        
        

    def initUI(self):
        # Créez un sous-conteneur 
        subContainer = QFrame(self)
        subContainer.setContentsMargins(0, 0, 0, 0)
        subContainer.setStyleSheet("background-color:#2c2c2c; color : white ;border: 0px ; padding: 9px;border-radius: 15px;")

        # Créez un layout pour le sous-conteneur
        subContainerLayout = QVBoxLayout(subContainer)

        # Créez un layout horizontal pour l'icône et le texte
        iconLabel = QLabel()
        topSpacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)
        subContainerLayout.addItem(topSpacer)
        iconLabel.setPixmap(QPixmap(r"C:\$Winkernel\formation python\mini_projet\app\prendre-des-notes.png"))
        iconLabel.setStyleSheet("padding-left:30px;")
        iconLabel.setAlignment(Qt.AlignCenter)

        # Ajoutez un message de bienvenue
        welcomeLabel = QLabel("Bienvenue !")
        welcomeLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        welcomeLabel.setAlignment(Qt.AlignCenter)

        # Ajoutez une description
        descriptionLabel = QLabel("""Gérez facilement vos enseignants et étudiants en ajoutant, modifiant et supprimant des profils. 
Suivez en temps réel les absences et les performances des élèves, avec un accès aux statistiques détaillées des notes et de la présence.""")
        descriptionLabel.setAlignment(Qt.AlignCenter)
        descriptionLabel.setWordWrap(True)

        # Ajoutez l'icône et le texte au layout horizontal
        subContainerLayout.addWidget(iconLabel)
        subContainerLayout.addWidget(welcomeLabel)
        subContainerLayout.addWidget(descriptionLabel)

        # Créez un layout principal pour le WelcomeWidget
        layout = QVBoxLayout(self)
        layout.addWidget(subContainer)

        self.setLayout(layout)
        bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        subContainerLayout.addItem(bottomSpacer)

    

class UserManagementWidget(QWidget):
    def __init__(self):
        super(UserManagementWidget, self).__init__()
        self.initUI()
        self.teste = 0
    
    def initUI(self):
        # Créez un sous-conteneur
        subContainer = QFrame(self)
        subContainer.setContentsMargins(0, 0, 0, 0)
        subContainer.setStyleSheet("background-color:white; color: black; border: 0px; padding: 15px; border-radius: 15px;")

        # Créez un layout pour le sous-conteneur
        subContainerLayout = QVBoxLayout(subContainer)
        subContainerLayout.setSpacing(0)

        # Ajoutez un titre
        titleLabel = QLabel("DashBoard", subContainer)
        titleLabel.setStyleSheet("font-size: 24px; color: black; padding: 15px;")
        titleLabel.setFixedHeight(50)
        titleLabel.setAlignment(Qt.AlignCenter)
        subContainerLayout.addWidget(titleLabel)

        # Créez et configurez la barre de recherche
        searchLayout = QHBoxLayout()
        searchLayout.setContentsMargins(0, 0, 0, 0)
        searchLayout.setSpacing(0)

        # Créer les boutons et le champ de saisie
        self.searchButton = QPushButton()
        self.searchButton.setFixedHeight(70)
        self.searchButton.setIcon(QIcon("recherche.png"))  # Mettez à jour le chemin vers l'icône
        self.searchButton.setIconSize(QSize(40, 40))
        self.userInput = QLineEdit()
        self.userInput.setFixedHeight(70)
        createUserButton = QPushButton()
        createUserButton.setFixedHeight(70)
        createUserButton.setIcon(QIcon("adduser.png"))  # Mettez à jour le chemin vers l'icône
        createUserButton.setIconSize(QSize(40, 40))
        buttonResearch = """QPushButton { border: 1px solid black;border-top-left-radius: 15px; 
                border-bottom-left-radius: 15px; 
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;padding px;}"""
        inputStyle = "QLineEdit { font-size:24px; border: 1px solid black; border-radius:0px; border-left: 0px;border-right: 0px;}"
        buttonAddUser = """QPushButton { border: 1px solid black;border-top-left-radius: 0px; 
                border-bottom-left-radius: 0px; 
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;}"""

        self.searchButton.setStyleSheet(buttonResearch)
        self.searchButton.clicked.connect(self.dashBoard)
        


        self.userInput.setStyleSheet(inputStyle)
        createUserButton.setStyleSheet(buttonAddUser)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addWidget(self.userInput)
        searchLayout.addWidget(createUserButton)
        subContainerLayout.addLayout(searchLayout)
        subContainerLayout.setSpacing(0)
        
        subContainerLayout.setSpacing(15)

        # Créez un nouveau conteneur pour le bloc supplémentaire
        additionalBlock = QFrame(subContainer)
        additionalBlock.setContentsMargins(0, 0, 0, 0)
        additionalBlock.setStyleSheet("background-color: white;color:black; border: 1px solid #c0c0c0; border-radius: 10px; padding: 0px;")
        self.additionalBlockLayout = QVBoxLayout(additionalBlock)
        self.additionalBlockLayout.setContentsMargins(0, 0, 0, 0)
        self.additionalBlockLayout.setSpacing(0)

        # Créer et configurer les labels de l'en-tête
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout.setSpacing(0)

        labels = ["Id", "Nom", "Prénom", "Type Utilisateur", "Paramètre 1", "Paramètre 2"]
        for text in labels:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: lightgray;color:black;font-weight: bold;margin: 0; border-radius : 0px;")
            if text=='Id':
                label.setStyleSheet("""background-color: lightgray;color:black;font-weight: bold;border-top-left-radius: 10px; 
                border-bottom-left-radius: 0px; 
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;margin: 0;""")
            elif text=='Paramètre 2':
                    label.setStyleSheet(""" background-color: lightgray;color:black;font-weight: bold ;border-top-left-radius: 0px; 
                border-bottom-left-radius: 0px; 
                border-top-right-radius: 10px;
                border-bottom-right-radius:0px;margin: 0;""")
            self.headerLayout.addWidget(label)
            label.setFixedHeight(70)
        self.additionalBlockLayout.addLayout(self.headerLayout)
        subContainerLayout.addWidget(additionalBlock)
        
        self.headerLayout.setSpacing(0)

        # subContainerLayout.addWidget(additionalBlock)

        # Définir le layout principal du widget
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(subContainer)
        self.setLayout(subContainerLayout)
        self.ResultLabel =QLabel()

    def dashBoard(self):
        # self.dashboard = QFrame(self.additionalBlockLayout)
        # self.dashboard.setStyleSheet(
        #                     "background-color: lightblue; color: black; "
        #                     "font-weight: bold; margin: 0; padding: 15px;border-radius:0px;"
        #                 )
        # dashboardLayout= QVBoxLayout(self.dashboard)
        # Supprimez tous les blocs d'entrée précédents.
        self.clear_input_blocks()

        search = self.userInput.text()
        if search == "" or self.sender() == self.searchButton :

            liste = AdminFeature().search_user(search)

            # Si la liste est vide, affichez "Aucun résultat" dans ResultLabel.
            if not liste:
                self.ResultLabel = QLabel()
                self.ResultLabel.setAlignment(Qt.AlignCenter)
                self.ResultLabel.setStyleSheet(
                            "background-color: lightblue; color: black; "
                            "font-weight: bold; margin: 0; padding: 15px;border-radius:0px;"
                        )
                self.additionalBlockLayout.addWidget(self.ResultLabel)
                self.ResultLabel.setText("Aucun résultat")
                self.ResultLabel.setVisible(True)  # Assurez-vous qu'il est visible
            else:
                # Cachez ResultLabel car nous avons des résultats à afficher
                for user in liste:
                    self.ResultLabel.setText("")
                    # Créez un bloc d'entrée pour chaque utilisateur
                    input_block = self.create_input_block(user["id"], user["username"].split(".")[0], user["username"].split(".")[1])
                    self.additionalBlockLayout.addLayout(input_block)

    def clear_input_blocks(self):
    # Supprimez tous les éléments du additionalBlockLayout sauf le headerLayout et le ResultLabel
        for i in reversed(range(self.additionalBlockLayout.count())):
            layout_item = self.additionalBlockLayout.itemAt(i)
            if layout_item.widget() is not None and layout_item.widget() is not self.ResultLabel:
                layout_item.widget().deleteLater()
            # Ne pas effacer le layout qui contient ResultLabel
            elif layout_item.layout() is not None and layout_item.layout() is not self.headerLayout:
                self.clear_layout(layout_item.layout())

    def clear_layout(self, layout):
        while layout.count():
            layout_item = layout.takeAt(0)
            widget = layout_item.widget()
            if widget is not None and widget is not self.ResultLabel:
                widget.deleteLater()
            elif layout_item.layout() is not None:
                self.clear_layout(layout_item.layout())
    def create_input_block(self, id_value, nom_value, prenom_value):
        inputLayout = QHBoxLayout()
        inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setSpacing(0)

        # Créez les champs de saisie et les boutons
        id_input = QLineEdit()
        id_input.setText(str(id_value))
        id_input.setAlignment(Qt.AlignCenter)
        id_input.setFixedHeight(30)  # Hauteur ajustée pour correspondre à votre style

        nom_input = QLineEdit()
        nom_input.setText(nom_value)
        nom_input.setAlignment(Qt.AlignCenter)
        nom_input.setFixedHeight(30)

        prenom_input = QLineEdit()
        prenom_input.setText(prenom_value)
        prenom_input.setAlignment(Qt.AlignCenter)
        prenom_input.setFixedHeight(30)

        # Ajoutez les champs de saisie au layout
        inputLayout.addWidget(id_input)
        inputLayout.addWidget(nom_input)
        inputLayout.addWidget(prenom_input)

        # Créez les boutons paramètre 1 et paramètre 2
        param1_button = QPushButton("Paramètre 1")
        param1_button.setFixedHeight(30)
        param2_button = QPushButton("Paramètre 2")
        param2_button.setFixedHeight(30)

        # Ajoutez les boutons au layout
        inputLayout.addWidget(param1_button)
        inputLayout.addWidget(param2_button)

        ("background-color: lightgray;color:black;font-weight: bold;margin: 0; border-radius : 0px;")

        
        return inputLayout

class PresenceWidget(QWidget):
    def __init__(self):
        super(PresenceWidget, self).__init__()
        self.initUI()

    def initUI(self):
        # Créez un sous-conteneur (par exemple, un QFrame)
        subContainer = QFrame(self)
        subContainer.setContentsMargins(0, 0, 0, 0)
        subContainer.setStyleSheet("background-color:white; color : white ;border: 0px ; padding: 9px;border-radius: 15px;")

        # Créez un layout pour le sous-conteneur
        subContainerLayout = QVBoxLayout(subContainer)
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(subContainer)

        # Appliquez le layout principal au UserManagementWidget
        self.setLayout(mainLayout)

class GradesWidget(QWidget):
    def __init__(self):
        super(GradesWidget, self).__init__()
        self.initUI()

    def initUI(self):
        # Créez un sous-conteneur (par exemple, un QFrame)
        subContainer = QFrame(self)
        subContainer.setContentsMargins(0, 0, 0, 0)
        subContainer.setStyleSheet("background-color:white; color : white ;border: 0px ; padding: 9px;border-radius: 15px;")

        # Créez un layout pour le sous-conteneur
        subContainerLayout = QVBoxLayout(subContainer)
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(subContainer)

        # Appliquez le layout principal au UserManagementWidget
        self.setLayout(mainLayout)

class FramelessWindow(QMainWindow):
    def __init__(self):
        self.activeButton = None
        self.ButonList=[]
        super(FramelessWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowMinimizeButtonHint |
                            Qt.WindowMaximizeButtonHint)
        self.setGeometry(100, 100, 1500, 700)
        self.setMinimumSize(650, 650)
        self.oldPos = None
        self.resizing = False

        # Icon Label
        self.iconLabel = QLabel(self)
        pixmap = QPixmap(r"C:\$Winkernel\formation python\mini_projet\app\Logo1.png")
        self.iconLabel.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio))
        self.iconLabel.setFixedSize(100, 50)
        self.iconLabel.setStyleSheet("background-color: #202020;padding-left: 25px;")

        # Tab Bar
        self.tabBar = QLabel("Interface Administrateur")
        self.tabBar.setStyleSheet("background-color: #202020; color: white; padding: 5px;font-size:20px")
        self.tabBar.setFixedHeight(50)
        self.tabBar.setContentsMargins(0, 0, 0, 0)

        # Buttons
        closeButton = QPushButton("X")
        closeButton.setFixedSize(50, 50)
        closeButton.setStyleSheet("QPushButton { background-color: #202020; color: white; "
                                  "font-weight: bold; border: none; } "
                                  "QPushButton:hover { background-color: red; }")
        closeButton.clicked.connect(self.close)
        
        minimizeButton = QPushButton("_")
        minimizeButton.setFixedSize(50, 50)
        minimizeButton.setStyleSheet("QPushButton { background-color: #202020; color: white; "
                                     "font-weight: bold; border: none; } "
                                     "QPushButton:hover { background-color: grey; }")
        minimizeButton.clicked.connect(self.showMinimized)
        
        resizeButton = QPushButton("[]")
        resizeButton.setFixedSize(50, 50)
        resizeButton.setStyleSheet("QPushButton { background-color: #202020; color: white; "
                                   "font-weight: bold; border: none; } "
                                   "QPushButton:hover { background-color: grey; }")
        resizeButton.clicked.connect(self.toggleMaximizeRestore)
        
        # Layout for buttons aligned with the tab bar
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(minimizeButton, 0, Qt.AlignTop)
        buttonsLayout.addWidget(resizeButton, 0, Qt.AlignTop)
        buttonsLayout.addWidget(closeButton, 0, Qt.AlignTop)
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        buttonsLayout.setSpacing(0)

        # Layout for the tab bar
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(self.iconLabel)
        tabLayout.addWidget(self.tabBar, 1)
        tabLayout.addLayout(buttonsLayout)
        tabLayout.setContentsMargins(0, 0, 0, 0)
        tabLayout.setSpacing(0)
        

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addLayout(tabLayout)
        mainLayout.setSpacing(3)
        
        

        # Central container
        self.centralContainer = QWidget()
        # self.centralContainer.setStyleSheet("background-color: #000;")

        # Layout for the central container
        centralContainerLayout = QHBoxLayout(self.centralContainer)
        centralContainerLayout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize and add the sidebar
        self.initSidebar()
        sidebarContainer = QWidget()
        sidebarContainer.setStyleSheet("background-color: #202020;")
        sidebarContainer.setLayout(self.sidebar)
        sidebarContainer.setFixedWidth(80)
        centralContainerLayout.addWidget(sidebarContainer)

        # Main content area
        self.initDashboard()
        self.mainContent = self.dashboardWidget
        centralContainerLayout.addWidget(self.mainContent)
        centralContainerLayout.setStretchFactor(self.mainContent, 1)

        # Add the central container to the main layout
        mainLayout.addWidget(self.centralContainer, 1)

        # Set the central widget
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        
        centralWidget.setStyleSheet("background-color: #202020;")
        centralWidget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(centralWidget)

        # self.welcomeWidget = WelcomeWidget()
        # self.userManagementWidget = UserManagementWidget()
        # self.presenceWidget = PresenceWidget()
        # self.gradesWidget = GradesWidget()

        # # Configurez le widget par défaut (Bienvenue)
        # self.setCentralWidget(self.welcomeWidget)
        
    def keyPressEvent(self, event):
        for i in range(3):
            self.ButonList[i].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                    border-radius : 15px;
                    font-weight: bold;
                    color: white;
                    padding: 0;
                }
            """)
        if event.key() == Qt.Key_Escape:
            # Si la touche Échap est pressée, affichez le WelcomeWidget
            self.stackedWidget.setCurrentWidget(self.welcomeWidget)

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
    def initDashboard(self):
        # Créez le widget de dashboard
        self.dashboardWidget = QWidget()
        self.dashboardWidget.setStyleSheet("""
            QWidget {
                /* Arrondir les bords du côté de la sidebar (gauche) et du haut */
                border-top-left-radius: 15px; 
                border-bottom-left-radius: 0px;
                /* Pas d'arrondi pour les bords droits */
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                /* Appliquez la couleur de fond et autres styles comme nécessaire */
                background-color: #2c2c2c; /* Remplacez par la couleur de fond de votre choix */
            }
        """)
        
        # Ajoutez le widget de dashboard au layout central
        dashboardLayout = QVBoxLayout(self.dashboardWidget)
        dashboardLayout.setSpacing(0)
        self.centralContainer.layout().addWidget(self.dashboardWidget)
        self.stackedWidget = QStackedWidget(self.dashboardWidget)
        

        # Ajoutez chaque widget que vous souhaitez afficher dans le QStackedWidget
        self.welcomeWidget = WelcomeWidget()
        self.userManagementWidget = UserManagementWidget()
        self.presenceWidget = PresenceWidget()
        self.gradesWidget = GradesWidget()

        self.stackedWidget.addWidget(self.welcomeWidget)
        self.stackedWidget.addWidget(self.userManagementWidget)
        self.stackedWidget.addWidget(self.presenceWidget)
        self.stackedWidget.addWidget(self.gradesWidget)

        # Configurez le widget par défaut (Bienvenue)
        self.stackedWidget.setCurrentWidget(self.welcomeWidget)
    
    # Ajoutez le QStackedWidget au layout du dashboard avec stretch=1
        dashboardLayout.addWidget(self.stackedWidget, stretch=1)

        

        # 

        # Ajoutez le widget de dashboard au layout central
        self.centralContainer.layout().addWidget(self.dashboardWidget)
    
    
    def initSidebar(self):
        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setSpacing(0)
        topSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.sidebar.addItem(topSpacer)

        # Création des boutons pour la sidebar
        icon_paths = [
            r'C:\$Winkernel\formation python\mini_projet\app\utilisateur.png',
            r'C:\$Winkernel\formation python\mini_projet\app\verifier.png',
            r'C:\$Winkernel\formation python\mini_projet\app\statistique.png'
        ]
        icon_sizes = [QSize(60, 60), QSize(55, 55), QSize(60, 60)]

        for i, icon_path in enumerate(icon_paths):
            # Créer un layout horizontal pour chaque bouton
            buttonLayout = QHBoxLayout()
            buttonLayout.setContentsMargins(0, 0, 0, 0)
            buttonLayout.setSpacing(0)

            # Créer un espaceur qui poussera le bouton vers la droite
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            buttonLayout.addItem(spacer)

            # Créer le bouton et le configurer
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(icon_sizes[i])
            btn.setFixedWidth(70)
            btn.setFixedHeight(70)
            btn.setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
            """)
            self.ButonList.append(btn)
            
            # Ajouter le bouton au layout horizontal
            buttonLayout.addWidget(btn)

            # Ajouter le layout horizontal au layout principal de la sidebar
            self.sidebar.addLayout(buttonLayout)
            if i == 0:
                btn.clicked.connect(lambda: self.showUserManagementWidget())
            elif i == 1:
                btn.clicked.connect(lambda : self.showPresenceWidget())
            elif i == 2:
                btn.clicked.connect(lambda: self.showGradesWidget())

        bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidebar.addItem(bottomSpacer)


    def showUserManagementWidget(self):

        self.ButonList[0].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                   background-color: #AAA;
                    border-radius : 15px;
                }
                
            """)
        self.ButonList[1].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                    border-radius : 15px;
                    font-weight: bold;
                    color: white;
                    padding: 0;
                }
            """)
        self.ButonList[2].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                    border-radius : 15px;
                    font-weight: bold;
                    color: white;
                    padding: 0;
                }
            """)
        
        
        self.stackedWidget.setCurrentWidget(self.userManagementWidget)
        self.userManagementWidget.dashBoard()
        

    def showPresenceWidget(self):
        self.ButonList[1].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                   background-color: #AAA;
                    border-radius : 15px;
                }
                
            """)
        self.ButonList[0].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                    border-radius : 15px;
                    font-weight: bold;
                    color: white;
                    padding: 0;
                }
            """)
        self.ButonList[2].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                    border-radius : 15px;
                    font-weight: bold;
                    color: white;
                    padding: 0;
                }
            """)
        self.stackedWidget.setCurrentWidget(self.presenceWidget)

    def showGradesWidget(self):
        self.ButonList[2].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                   background-color: #AAA;
                    border-radius : 15px;
                }
                
            """)
        self.ButonList[1].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                    border-radius : 15px;
                    font-weight: bold;
                    color: white;
                    padding: 0;
                }
            """)
        self.ButonList[0].setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    color: white;
                    padding: 0;
                    background-color: #202020;
                    border-radius : 15px;
                }
                QPushButton:hover {
                    background-color: #555;
                    border-radius : 15px;
                    font-weight: bold;
                    color: white;
                    padding: 0;
                }
            """)
        self.stackedWidget.setCurrentWidget(self.presenceWidget)
    
            
if __name__ == "__main__":
    app = QApplication([])
    window = FramelessWindow()
    window.show()
    app.exec_()