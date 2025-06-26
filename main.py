import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_Form  # Importation de la classe d'interface générée par Qt Designer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Création d'une instance de l'interface utilisateur
        self.ui = Ui_Form()  # Remplacer par Ui_MainWindow() si nécessaire
        # Configuration de l'interface utilisateur dans la fenêtre principale
        self.ui.setupUi(self)

if __name__ == '__main__':
    # Création de l'application Qt
    # sys.argv est une liste des arguments de la ligne de commande passés au script Python.
    # Par exemple, si vous exécutez : python main.py foo bar
    # alors sys.argv vaudra ['main.py', 'foo', 'bar']
    # QApplication utilise sys.argv pour gérer les arguments spécifiques à Qt (comme le style ou la langue).
    app = QApplication(sys.argv)
    # Création de la fenêtre principale
    window = MainWindow()
    # Affichage de la fenêtre principale
    window.show()
    # Exécution de la boucle principale de l'application
    sys.exit(app.exec())
