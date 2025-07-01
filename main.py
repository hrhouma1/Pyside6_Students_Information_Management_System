import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from main_ui import Ui_Form
from connect_database import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Création d'une instance de l'interface utilisateur
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Initialisation de la base de données
        self.db_manager = DatabaseManager()
        
        # Configuration initiale
        self.setup_ui()
        self.connect_signals()
        self.load_students()
        
    def setup_ui(self):
        """Configuration initiale de l'interface utilisateur"""
        # Configuration du tableau
        self.ui.tableWidget.setSelectionBehavior(self.ui.tableWidget.SelectionBehavior.SelectRows)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Rendre le ComboBox City éditable pour permettre la saisie libre
        self.ui.comboBox_2.setEditable(True)
        self.ui.comboBox_2.setInsertPolicy(self.ui.comboBox_2.InsertPolicy.NoInsert)
        
        # Charger les provinces dans le ComboBox
        self.load_states()
        
    def connect_signals(self):
        """Connexion des signaux des boutons aux fonctions"""
        self.ui.add_btn.clicked.connect(self.add_student)
        self.ui.update_btn.clicked.connect(self.update_student)
        self.ui.select_btn.clicked.connect(self.select_student)
        self.ui.search_btn.clicked.connect(self.search_students)
        self.ui.clear_btn.clicked.connect(self.clear_fields)
        self.ui.delete_btn.clicked.connect(self.delete_student)
        
        # Signal pour la sélection dans le tableau
        self.ui.tableWidget.itemSelectionChanged.connect(self.on_table_selection_changed)
        
        # Signal pour le changement de province dans le ComboBox
        self.ui.comboBox.currentTextChanged.connect(self.on_state_changed)
    
    def load_states(self):
        """Charger les provinces dans le ComboBox"""
        states = self.db_manager.get_states()
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(states)
        
        # Ajouter quelques provinces canadiennes par défaut si la base est vide
        if not states:
            default_provinces = ["Québec", "Ontario", "Colombie-Britannique", "Alberta", "Manitoba", "Saskatchewan", "Nouvelle-Écosse", "Nouveau-Brunswick"]
            self.ui.comboBox.addItems(default_provinces)
    
    def on_state_changed(self, state):
        """Mettre à jour les villes quand la province change"""
        if state:
            cities = self.db_manager.get_cities_by_state(state)
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(cities)
            
            # Ajouter des villes canadiennes par défaut selon la province
            if not cities:
                province_cities = {
                    "Québec": ["Montréal", "Québec", "Laval", "Gatineau", "Longueuil", "Sherbrooke"],
                    "Ontario": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London", "Windsor"],
                    "Colombie-Britannique": ["Vancouver", "Victoria", "Surrey", "Burnaby", "Richmond"],
                    "Alberta": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat"],
                    "Manitoba": ["Winnipeg", "Brandon", "Steinbach", "Thompson"],
                    "Saskatchewan": ["Saskatoon", "Regina", "Prince Albert", "Moose Jaw"],
                    "Nouvelle-Écosse": ["Halifax", "Sydney", "Dartmouth", "Truro"],
                    "Nouveau-Brunswick": ["Moncton", "Saint John", "Fredericton", "Dieppe"]
                }
                
                default_cities = province_cities.get(state, ["Montréal", "Toronto", "Vancouver"])
                self.ui.comboBox_2.addItems(default_cities)
    
    def load_students(self):
        """Charger tous les étudiants dans le tableau"""
        students = self.db_manager.get_all_students()
        self.populate_table(students)
    
    def populate_table(self, students):
        """Remplir le tableau avec les données des étudiants"""
        self.ui.tableWidget.setRowCount(len(students))
        
        for row, student in enumerate(students):
            # student = (student_id, first_name, last_name, city, state, email)
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(student[0])))  # Student ID
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(student[1]))       # First Name
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(student[2]))       # Last Name
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(student[3]))       # City
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(student[4]))       # State
            self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(student[5]))       # Email
    
    def get_form_data(self):
        """Récupérer les données du formulaire"""
        return {
            'first_name': self.ui.lineEdit_2.text().strip(),   # lineEdit_2 = First Name
            'last_name': self.ui.lineEdit_3.text().strip(),    # lineEdit_3 = Last Name  
            'email': self.ui.lineEdit_6.text().strip(),        # lineEdit_6 = Email Address
            'state': self.ui.comboBox.currentText(),
            'city': self.ui.comboBox_2.currentText().strip()   # .strip() pour supprimer espaces
        }
    
    def validate_form_data(self, data):
        """Valider les données du formulaire"""
        if not all([data['first_name'], data['last_name'], data['email'], data['state'], data['city']]):
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires!")
            return False
        
        # Validation améliorée de l'email
        email = data['email'].strip()
        
        # Vérifier que l'email contient @ et au moins un point après @
        if '@' not in email:
            QMessageBox.warning(self, "Erreur", "L'email doit contenir '@'")
            return False
        
        # Séparer la partie avant et après @
        parts = email.split('@')
        if len(parts) != 2:
            QMessageBox.warning(self, "Erreur", "L'email ne peut contenir qu'un seul '@'")
            return False
        
        local_part, domain_part = parts
        
        # Vérifier que les parties ne sont pas vides
        if not local_part or not domain_part:
            QMessageBox.warning(self, "Erreur", "L'email doit avoir du texte avant et après '@'")
            return False
        
        # Vérifier que le domaine contient au moins un point
        if '.' not in domain_part:
            QMessageBox.warning(self, "Erreur", "Le domaine de l'email doit contenir un point (ex: .com, .fr)")
            return False
        
        # Vérifier qu'il n'y a pas de double point
        if '..' in email:
            QMessageBox.warning(self, "Erreur", "L'email ne peut pas contenir de double point")
            return False
        
        # Vérifier que ça ne commence/finit pas par @ ou .
        if email.startswith('@') or email.startswith('.') or email.endswith('@') or email.endswith('.'):
            QMessageBox.warning(self, "Erreur", "L'email ne peut pas commencer ou finir par '@' ou '.'")
            return False
        
        return True
    
    def add_student(self):
        """Ajouter un nouvel étudiant"""
        data = self.get_form_data()
        
        if not self.validate_form_data(data):
            return
        
        success = self.db_manager.add_student(
            data['first_name'],
            data['last_name'],
            data['city'],
            data['state'],
            data['email']
        )
        
        if success:
            QMessageBox.information(self, "Succès", "Étudiant ajouté avec succès!")
            self.clear_fields()
            self.load_students()
            self.load_states()  # Recharger les provinces au cas où une nouvelle serait ajoutée
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de l'ajout de l'étudiant!")
    
    def update_student(self):
        """Mettre à jour un étudiant existant"""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un étudiant à modifier!")
            return
        
        student_id = int(self.ui.tableWidget.item(selected_row, 0).text())
        data = self.get_form_data()
        
        if not self.validate_form_data(data):
            return
        
        success = self.db_manager.update_student(
            student_id,
            data['first_name'],
            data['last_name'],
            data['city'],
            data['state'],
            data['email']
        )
        
        if success:
            QMessageBox.information(self, "Succès", "Étudiant mis à jour avec succès!")
            self.clear_fields()
            self.load_students()
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de la mise à jour de l'étudiant!")
    
    def select_student(self):
        """Sélectionner et charger les données d'un étudiant"""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un étudiant!")
            return
        
        # Charger les données dans le formulaire
        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(selected_row, 1).text())  # First Name
        self.ui.lineEdit_3.setText(self.ui.tableWidget.item(selected_row, 2).text())  # Last Name
        self.ui.lineEdit_6.setText(self.ui.tableWidget.item(selected_row, 5).text())  # Email
        
        # Définir la province et la ville
        state = self.ui.tableWidget.item(selected_row, 4).text()
        city = self.ui.tableWidget.item(selected_row, 3).text()
        
        # Trouver et sélectionner la province
        state_index = self.ui.comboBox.findText(state)
        if state_index != -1:
            self.ui.comboBox.setCurrentIndex(state_index)
        
        # Définir la ville (dans le ComboBox éditable)
        city_index = self.ui.comboBox_2.findText(city)
        if city_index != -1:
            self.ui.comboBox_2.setCurrentIndex(city_index)
        else:
            # Si la ville n'est pas dans la liste, la taper directement
            self.ui.comboBox_2.setEditText(city)
    
    def search_students(self):
        """Rechercher des étudiants"""
        search_term = self.ui.lineEdit_7.text().strip()  # Utiliser lineEdit_7 pour la recherche
        if not search_term:
            self.load_students()  # Charger tous les étudiants si pas de terme de recherche
            return
        
        students = self.db_manager.search_students(search_term)
        self.populate_table(students)
        
        if not students:
            QMessageBox.information(self, "Recherche", "Aucun étudiant trouvé avec ce terme de recherche.")
    
    def clear_fields(self):
        """Vider tous les champs du formulaire"""
        self.ui.lineEdit_2.clear()  # First Name
        self.ui.lineEdit_3.clear()  # Last Name
        self.ui.lineEdit_6.clear()  # Email Address
        self.ui.lineEdit_7.clear()  # Search field
        if self.ui.comboBox.count() > 0:
            self.ui.comboBox.setCurrentIndex(0)
        # Vider le ComboBox City éditable
        self.ui.comboBox_2.clearEditText()
        if self.ui.comboBox_2.count() > 0:
            self.ui.comboBox_2.setCurrentIndex(0)
    
    def delete_student(self):
        """Supprimer un étudiant"""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un étudiant à supprimer!")
            return
        
        student_id = int(self.ui.tableWidget.item(selected_row, 0).text())
        student_name = f"{self.ui.tableWidget.item(selected_row, 1).text()} {self.ui.tableWidget.item(selected_row, 2).text()}"
        
        # Demander confirmation
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'étudiant {student_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.db_manager.delete_student(student_id)
            if success:
                QMessageBox.information(self, "Succès", "Étudiant supprimé avec succès!")
                self.load_students()
                self.clear_fields()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la suppression de l'étudiant!")
    
    def on_table_selection_changed(self):
        """Gérer les changements de sélection dans le tableau"""
        # Cette fonction peut être utilisée pour des actions automatiques
        # quand une ligne est sélectionnée
        pass

if __name__ == '__main__':
    # Création de l'application Qt
    app = QApplication(sys.argv)
    # Création de la fenêtre principale
    window = MainWindow()
    # Affichage de la fenêtre principale
    window.show()
    # Exécution de la boucle principale de l'application
    sys.exit(app.exec())
