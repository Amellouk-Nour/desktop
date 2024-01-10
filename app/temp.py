from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QFrame, QLineEdit, QTableWidget, QTableWidgetItem
from PySide2.QtCore import Qt, QPoint, QRect, QSize
from PySide2.QtGui import QCursor, QPixmap, QIcon
from tinydb import TinyDB, Query
import json,re
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


class UserManagementWidget(QWidget):
    def __init__(self):
        super(UserManagementWidget, self).__init__()
        
        
        self.initUI()
    
    def initUI(self):
        # Créez un sous-conteneur (par exemple, un QFrame)
        subContainer = QFrame(self)
        subContainer.setContentsMargins(0, 0, 0, 0)
        subContainer.setStyleSheet("background-color:white; color: black; border: 0px; padding: 15px; border-radius: 15px;")

        # Créez un layout pour le sous-conteneur
        subContainerLayout = QVBoxLayout(subContainer)

        # Ajoutez un titre
        titleLabel = QLabel("DashBoard", subContainer)
        titleLabel.setStyleSheet("font-size: 24px; color: black;")
        titleLabel.setFixedHeight(70)
        titleLabel.setAlignment(Qt.AlignCenter)
        subContainerLayout.addWidget(titleLabel)

        # Créez et configurez la barre de recherche
        searchLayout = QHBoxLayout()
        searchLayout.setContentsMargins(0, 0, 0, 0)
        searchLayout.setSpacing(0)
        
        

    # Créer les boutons et le champ de saisie
        self.searchButton = QPushButton()
        self.searchButton.setFixedHeight(70)
        self.searchButton.setIcon(QIcon(r"C:\$Winkernel\formation python\mini_projet\app\recherche.png"))
        self.searchButton.setIconSize(QSize(40, 40))
        self.userInput = QLineEdit()
        self.userInput.setFixedHeight(70)
        createUserButton = QPushButton()
        createUserButton.setFixedHeight(70)
        createUserButton.setIcon(QIcon(r"C:\$Winkernel\formation python\mini_projet\app\adduser.png"))
        createUserButton.setIconSize(QSize(40, 40))
        createUserButton.setFixedHeight(70)
        buttonResearch = """QPushButton { border: 1px solid black;border-top-left-radius: 15px; 
                border-bottom-left-radius: 15px; 
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;}"""
        inputStyle = "QLineEdit { font-size:24px; border: 1px solid black; border-radius:0px; border-left: 0px;border-right: 0px;}"
        buttonAddUser = """QPushButton { border: 1px solid black;border-top-left-radius: 0px; 
                border-bottom-left-radius: 0px; 
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;}"""

        self.searchButton.setStyleSheet(buttonResearch)
        self.searchButton.clicked.connect(self.dashBoard)
        
       
        
        self.userInput.setStyleSheet(inputStyle)
        createUserButton.setStyleSheet(buttonAddUser)

        # Ajouter les widgets au layout horizontal
        searchLayout.addWidget(self.searchButton)
        searchLayout.addWidget(self.userInput)
        searchLayout.addWidget(createUserButton)
          # Set the style for the title
        subContainerLayout.addLayout(searchLayout)

    # Créez un nouveau conteneur pour le bloc supplémentaire
        additionalBlock = QFrame(subContainer)
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

        self.dashBoard()

       
        # Ajoutez le layout principal à votre widget
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(subContainer)
        self.setLayout(mainLayout)
        self.ResultLabel = QLabel()
    def dashBoard(self):
        self.clear_input_blocks()

        search = self.userInput.text()
        if search == "" or self.sender() == self.searchButton :

            liste = AdminFeature().search_user(search)

            # Si la liste est vide, affichez "Aucun résultat" dans ResultLabel.
            if not liste:
                
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
        
if __name__ == "__main__":
    app = QApplication([])
    window = UserManagementWidget()
    window.show()
    app.exec_()