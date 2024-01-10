import sys, time
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PySide2.QtGui import QPixmap, QMouseEvent
from PySide2.QtCore import Qt, QSize, QPoint, QTimer
from tinydb import TinyDB, Query
from PySide2.QtCore import QEvent
import Admin

db = TinyDB('dataBase.json', indent = 4)
utilisateurs = db.table('Users')

def verify_user(username, password):
        User = Query()
        user_data = utilisateurs.search(User.username == username)

        if user_data:
            stored_password = user_data[0]['password']

            if password.encode('utf-8')== stored_password.encode('utf-8'):
                return (1, 1, user_data[0]['permission'])
            else :
                return (1, 0, None)
        return (0, 0, None)

# ligne pour créer l'administrateur
# utilisateurs.insert({'username': "admin", 'password':"root", 'email': None,"permission":1})

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurer la fenêtre
        self.setWindowTitle('Ecole central Casablanca : System de scolarité')
        self.setStyleSheet("QWidget { background-color: #A9D0F5; }")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Supprimer la bordure et la barre de titre standard
        self.setMinimumSize(QSize(500, 300))  # Ajuster la taille au besoin
        self.oldPos = None
        # Bouton de fermeture
        self.close_button = QPushButton('X')
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 100px;
                background-color: red;
                color: white;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        self.close_button.setFixedSize(30, 30)

        # Label centré
        title_label = QLabel('Connectez-vous !')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("QLabel { font-size: 24px; }")
        
        # Layout pour le titre centré
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)

        # Layout supérieur pour le titre et le bouton de fermeture
        top_layout = QHBoxLayout()
        top_layout.addLayout(title_layout, 1)
        top_layout.addWidget(self.close_button, 0, Qt.AlignTop | Qt.AlignRight)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)

        # Layout horizontal pour l'image et les champs de connexion
        h_layout = QHBoxLayout()

        # Ajouter une QLabel pour l'image
        self.image_label = QLabel()
        self.pixmap = QPixmap('1.jpg').scaled(400, 200, Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(self.image_label)

        
        # Layout vertical pour les champs de saisie
        fields_layout = QVBoxLayout()
        fields_layout .addSpacing(40)
        username_label = QLabel('Nom de l\'Utilisateur')
        username_label.setAlignment(Qt.AlignCenter)
        fields_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.installEventFilter(self)
        self.username_input.setPlaceholderText('Entrez votre email ou nom d\'utilisateur')
        self.username_input.setStyleSheet("QLineEdit { border-radius: 10px; padding: 5px; background-color: #FFFFFF;}")
        fields_layout.addWidget(self.username_input)

        password_label = QLabel('Mot de passe')
        password_label.setAlignment(Qt.AlignCenter)
        fields_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.installEventFilter(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Entrez votre mot de passe')
        self.password_input.setStyleSheet("QLineEdit { border-radius: 10px; padding: 5px; background-color: #FFFFFF;}")
        fields_layout.addWidget(self.password_input)
        fields_layout.addSpacing(1)  

        self.error_message_label = QLabel('')
        self.error_message_label.setAlignment(Qt.AlignCenter)
        
        fields_layout.addWidget(self.error_message_label)

        login_button_layout = QHBoxLayout()
        login_button_layout.addStretch()  
        self.login_button = QPushButton('Connexion')
        self.login_button.clicked.connect(self.on_login_clicked)
        self.login_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 5px;
                background-color: #003366;  /* Bleu foncé */
                color: white;              /* Texte en blanc */
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004080;  /* Un peu plus clair lors du survol */
            }
        """)
        self.login_button.setFixedWidth(100)  # Définir une largeur fixe pour le bouton
        login_button_layout.addWidget(self.login_button)
        login_button_layout.addStretch()  # Espace vide pour centrer le bouton

        fields_layout.addLayout(login_button_layout)
        fields_layout.addWidget(self.login_button)

        h_layout.addLayout(fields_layout)
        main_layout.addLayout(h_layout)
        self.setLayout(main_layout)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self.username_input:
                self.on_focus_username_input()  # Appeler lors du focus sur username_input
            elif obj == self.password_input:
                self.on_focus_password_input()  # Appeler lors du focus sur password_input

        return super().eventFilter(obj, event)

    
    def on_focus_username_input(self):
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;  /* Couleur de fond par défaut */
                border-radius: 10px; padding: 5px;
            }
            QLineEdit:focus {
                border-radius: 10px; padding: 5px;
                background-color: #FFFFFF;  /* Couleur de fond reste inchangée lors du focus */
            }
        """)
    def on_focus_password_input(self):
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;  /* Couleur de fond par défaut */
                border-radius: 10px; padding: 5px;
            }
            QLineEdit:focus {
                border-radius: 10px; padding: 5px;
                background-color: #FFFFFF;  /* Couleur de fond reste inchangée lors du focus */
            }
        """)
    
    def mousePressEvent(self, event: QMouseEvent):
        # Enregistre la position actuelle du curseur
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.oldPos:
            # Calcule le déplacement
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
    def launchAdminWindow(self):
        # Importez le deuxième script ici, si nécessaire
        self.adminWindow = Admin.FramelessWindow()  # Créez une instance de la fenêtre d'administration
        self.adminWindow.show() 
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.oldPos = None
    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if verify_user(username,password)[0]:
            self.error_message_label.setText('')
            self.username_input.setStyleSheet("""QLineEdit {
        border-radius: 10px;
        padding: 5px;
        background-color:#A0FFA0 ;  /* Couleur de fond par défaut */
    }""")
        else :
             self.error_message_label.setStyleSheet("QLabel { color: red; font-size: 14px; }")
             self.error_message_label.setText('Réessayer')
             self.username_input.setStyleSheet("""QLineEdit {
        border-radius: 10px;
        padding: 5px;
        background-color:#FF0000 ;  /* Couleur de fond par défaut */
    }
    QLineEdit:focus {
        background-color: #FFFFFF;  /* Couleur de fond lors de la saisie (rouge) */
    }
            """)
        if verify_user(username,password)[1]:
            self.error_message_label.setText('')
            self.password_input.setStyleSheet("""QLineEdit {
        border-radius: 10px;
        padding: 5px;
        background-color:#A0FFA0 ;  /* Couleur de fond par défaut */
    }""")
            
        else :
             self.error_message_label.setStyleSheet("QLabel { color: red; font-size: 14px; }")
             self.error_message_label.setText('Réessayer')
             self.password_input.setStyleSheet("""
        QLineEdit {
        border-radius: 10px;
        padding: 5px;
        background-color:#FF0000 ;  /* Couleur de fond par défaut */
    }
    QLineEdit:focus {
        background-color: #FFFFFF;  /* Couleur de fond lors de la saisie (rouge) */
    }
            """)
        if verify_user(username,password)[2]:
            self.error_message_label.setStyleSheet("QLabel { color: black; font-size: 14px; }")
            self.error_message_label.setText('Bienvenue !')
            
            # Attendre 2 secondes avant de continuer
            if verify_user(username,password)[2]==1 :
                QTimer.singleShot(1000, self.ferm_ouvrir_interface_Admin)
                  # Lancez la fenêtre d'administration
    def ferm_ouvrir_interface_Admin(self):
        self.launchAdminWindow()
        self.close()

# Créer l'application Qt
if __name__=="__main__":
     
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())