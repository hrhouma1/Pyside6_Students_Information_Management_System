# Guide Partie 3 : Modifications Interface - main.py

## Transformation complète du fichier main.py

### **AVANT** (Version originale - 26 lignes)
```python
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
```

### **APRÈS** (Version avec base de données - 200+ lignes)

---

## Lignes 1-4 : Imports étendus

### **AVANT :**
```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_Form  # Importation de la classe d'interface générée par Qt Designer
```

### **APRÈS :**
```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from main_ui import Ui_Form
from connect_database import DatabaseManager
```

### **Modifications détaillées :**

**Ligne 2 - Ajouts :**
- `QMessageBox` : Pour les boîtes de dialogue (succès, erreur, confirmation)
- `QTableWidgetItem` : Pour créer les éléments du tableau
- `QHeaderView` : Pour configurer les en-têtes de colonnes

**Ligne 4 - Nouveau :**
- `from connect_database import DatabaseManager` : Import du module créé

---

## Lignes 6-20 : Constructeur transformé

### **AVANT :**
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Création d'une instance de l'interface utilisateur
        self.ui = Ui_Form()  # Remplacer par Ui_MainWindow() si nécessaire
        # Configuration de l'interface utilisateur dans la fenêtre principale
        self.ui.setupUi(self)
```

### **APRÈS :**
```python
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
```

### **Modifications ligne par ligne :**

**Ligne 9** : Commentaire simplifié  
**Ligne 10** : Suppression du commentaire inutile

**Ligne 13-14 : AJOUTÉ**
```python
# Initialisation de la base de données
self.db_manager = DatabaseManager()
```
- **Instance BDD** : Stockée comme attribut de classe
- **Disponible partout** : Accessible dans toutes les méthodes via `self.db_manager`

**Lignes 16-19 : AJOUTÉ**
```python
# Configuration initiale
self.setup_ui()
self.connect_signals()
self.load_students()
```
- **setup_ui()** : Configuration spéciale de l'interface
- **connect_signals()** : Connexion boutons ↔ fonctions
- **load_students()** : Chargement initial des données

---

## Lignes 21-30 : Configuration UI (NOUVEAU)

```python
def setup_ui(self):
    """Configuration initiale de l'interface utilisateur"""
    # Configuration du tableau
    self.ui.tableWidget.setSelectionBehavior(self.ui.tableWidget.SelectionBehavior.SelectRows)
    self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    # Charger les états dans le ComboBox
    self.load_states()
```

### **Analyse détaillée :**

**Ligne 24 :** `setSelectionBehavior(SelectRows)`
- **Sélection par ligne** : Quand on clique, toute la ligne est sélectionnée
- **Alternative** : SelectItems (cellule par cellule)
- **Ergonomie** : Plus facile pour l'utilisateur

**Ligne 25 :** `setSectionResizeMode(Stretch)`
- **Colonnes extensibles** : Se redimensionnent automatiquement
- **Remplit la largeur** : Utilise tout l'espace disponible
- **`QHeaderView`** : Nécessite l'import ligne 2

**Ligne 28 :** `self.load_states()`
- **Chargement initial** : Remplit le ComboBox des états
- **Depuis la BDD** : Utilise les données existantes

---

## Lignes 32-45 : Connexion des signaux (NOUVEAU)

```python
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
    
    # Signal pour le changement d'état dans le ComboBox
    self.ui.comboBox.currentTextChanged.connect(self.on_state_changed)
```

### **Mécanisme Signal-Slot Qt :**

**Lignes 34-39 : Boutons → Fonctions**
- **Pattern Qt** : `widget.signal.connect(slot)`
- **clicked** : Signal émis lors du clic
- **self.add_student** : Fonction (slot) à exécuter

**Ligne 42 : Signal tableau**
```python
self.ui.tableWidget.itemSelectionChanged.connect(self.on_table_selection_changed)
```
- **itemSelectionChanged** : Émis quand la sélection change
- **Actuellement vide** : Fonction présente pour extension future

**Ligne 45 : Signal ComboBox**
```python
self.ui.comboBox.currentTextChanged.connect(self.on_state_changed)
```
- **currentTextChanged** : Émis quand l'utilisateur change la sélection
- **État → Villes** : Met à jour automatiquement les villes

---

## Lignes 47-55 : Chargement des états (NOUVEAU)

```python
def load_states(self):
    """Charger les états dans le ComboBox"""
    states = self.db_manager.get_states()
    self.ui.comboBox.clear()
    self.ui.comboBox.addItems(states)
    
    # Ajouter quelques états par défaut si la base est vide
    if not states:
        default_states = ["Île-de-France", "Provence-Alpes-Côte d'Azur", "Occitanie", "Nouvelle-Aquitaine", "Auvergne-Rhône-Alpes"]
        self.ui.comboBox.addItems(default_states)
```

### **Logique intelligente :**

**Ligne 49 :** `states = self.db_manager.get_states()`
- **Appel BDD** : Récupère les états uniques depuis la table
- **Liste dynamique** : Basée sur les données réelles

**Ligne 50 :** `self.ui.comboBox.clear()`
- **Nettoyage** : Supprime les anciens éléments
- **Évite les doublons** : À chaque rechargement

**Ligne 51 :** `self.ui.comboBox.addItems(states)`
- **addItems()** : Ajoute une liste d'éléments
- **Alternative** : addItem() pour un élément unique

**Lignes 53-55 : États par défaut**
```python
if not states:
    default_states = ["Île-de-France", "Provence-Alpes-Côte d'Azur", "Occitanie", "Nouvelle-Aquitaine", "Auvergne-Rhône-Alpes"]
    self.ui.comboBox.addItems(default_states)
```
- **Base vide** : Si aucun étudiant, pas d'états dans la BDD
- **UX** : L'utilisateur peut quand même sélectionner un état
- **Bootstrap** : Permet d'ajouter le premier étudiant

---

## Lignes 57-68 : Mise à jour des villes (NOUVEAU)

```python
def on_state_changed(self, state):
    """Mettre à jour les villes quand l'état change"""
    if state:
        cities = self.db_manager.get_cities_by_state(state)
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(cities)
        
        # Ajouter quelques villes par défaut si aucune n'est trouvée
        if not cities:
            default_cities = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]
            self.ui.comboBox_2.addItems(default_cities)
```

### **Cascade dynamique État → Ville :**

**Ligne 57 :** `def on_state_changed(self, state):`
- **Paramètre state** : Valeur automatiquement passée par Qt
- **Signal currentTextChanged** : Envoie le nouveau texte

**Ligne 59 :** `if state:`
- **Vérification** : État non vide
- **Évite** : Appels BDD inutiles

**Ligne 60 :** `cities = self.db_manager.get_cities_by_state(state)`
- **Requête filtrée** : Seules les villes de cet état
- **Méthode BDD** : Définie dans connect_database.py

**Logique similaire** aux états pour les villes par défaut

---

## Lignes 72-95 : Remplissage du tableau (NOUVEAU)

```python
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
```

### **Mapping BDD → Interface :**

**Ligne 74 :** `self.ui.tableWidget.setRowCount(len(students))`
- **Dimensionnement** : Prépare le bon nombre de lignes
- **Performance** : Évite le redimensionnement dynamique

**Ligne 76 :** `for row, student in enumerate(students):`
- **enumerate()** : Donne index (row) et valeur (student)
- **student** : Tuple (id, prénom, nom, ville, état, email)

**Lignes 78-83 : Mapping des colonnes**
```python
# student = (student_id, first_name, last_name, city, state, email)
#              [0]         [1]         [2]       [3]    [4]     [5]
```

**Ligne 78 :** `QTableWidgetItem(str(student[0]))`
- **student[0]** : student_id (INTEGER)
- **str()** : Conversion en string pour affichage
- **QTableWidgetItem** : Objet Qt pour cellule de tableau

**Lignes 79-83 :** Même principe pour les autres colonnes
- **Pas de str()** : Les autres champs sont déjà TEXT

---

## Lignes 97-106 : Récupération données formulaire (NOUVEAU)

```python
def get_form_data(self):
    """Récupérer les données du formulaire"""
    return {
        'first_name': self.ui.lineEdit.text().strip(),
        'last_name': self.ui.lineEdit_2.text().strip(),
        'email': self.ui.lineEdit_3.text().strip(),
        'state': self.ui.comboBox.currentText(),
        'city': self.ui.comboBox_2.currentText()
    }
```

### **Centralisation des données :**

**Retour dictionnaire :**
- **Structure claire** : Clés parlantes
- **Réutilisable** : Même format pour add/update

**Ligne 100 :** `.text().strip()`
- **.text()** : Récupère le contenu du QLineEdit
- **.strip()** : Supprime espaces début/fin

**Ligne 104-105 :** `.currentText()`
- **ComboBox** : Récupère l'élément sélectionné
- **String** : Pas de strip() car sélection dans liste

---

## Lignes 108-120 : Validation des données (NOUVEAU)

```python
def validate_form_data(self, data):
    """Valider les données du formulaire"""
    if not all([data['first_name'], data['last_name'], data['email'], data['state'], data['city']]):
        QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires!")
        return False
    
    # Validation basique de l'email
    if '@' not in data['email'] or '.' not in data['email']:
        QMessageBox.warning(self, "Erreur", "Format d'email invalide!")
        return False
    
    return True
```

### **Validations côté client :**

**Ligne 110 :** `all([data['first_name'], data['last_name'], ...])`
- **all()** : True si tous les éléments sont "truthy"
- **String vide ""** : Considérée comme False
- **Vérification complète** : Tous les champs obligatoires

**Ligne 111 :** `QMessageBox.warning(self, "Erreur", "...")`
- **QMessageBox.warning** : Boîte de dialogue d'erreur
- **Paramètres** : parent, titre, message
- **Bloque l'interface** : Utilisateur doit cliquer OK

**Lignes 114-116 : Validation email**
```python
if '@' not in data['email'] or '.' not in data['email']:
```
- **Validation basique** : Présence @ ET .
- **Pas regex** : Suffisant pour ce projet éducatif
- **Production** : Utiliserait regex complète

---

## Lignes 122-143 : Ajout d'étudiant (NOUVEAU)

```python
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
        self.load_states()  # Recharger les états au cas où un nouveau serait ajouté
    else:
        QMessageBox.warning(self, "Erreur", "Erreur lors de l'ajout de l'étudiant!")
```

### **Workflow complet :**

**Lignes 124-126 : Préparation**
```python
data = self.get_form_data()
if not self.validate_form_data(data):
    return
```
- **Récupération** : Données du formulaire
- **Validation** : Côté client d'abord
- **Sortie précoce** : Si validation échoue

**Lignes 128-134 : Appel BDD**
```python
success = self.db_manager.add_student(
    data['first_name'],
    data['last_name'],
    data['city'],
    data['state'],
    data['email']
)
```
- **Ordre paramètres** : Correspond à la signature de add_student()
- **Retour boolean** : True/False selon succès

**Lignes 136-141 : Actions post-succès**
```python
if success:
    QMessageBox.information(self, "Succès", "Étudiant ajouté avec succès!")
    self.clear_fields()
    self.load_students()
    self.load_states()
```
- **Message succès** : Feedback utilisateur
- **clear_fields()** : Vide le formulaire
- **load_students()** : Recharge le tableau
- **load_states()** : Recharge les ComboBox (peut y avoir nouveau état)

---

## Pattern récurrent dans toutes les opérations

### Structure type d'une opération CRUD :

```python
def operation_student(self):
    # 1. Récupération des données
    data = self.get_form_data()
    
    # 2. Validation côté client
    if not self.validate_form_data(data):
        return
    
    # 3. Appel base de données
    success = self.db_manager.operation_method(...)
    
    # 4. Feedback utilisateur
    if success:
        QMessageBox.information(self, "Succès", "...")
        self.clear_fields()
        self.load_students()
    else:
        QMessageBox.warning(self, "Erreur", "...")
```

### Avantages de cette approche :

1. **Séparation des responsabilités** : Interface ↔ BDD
2. **Validation double** : Client + Serveur (BDD)
3. **Feedback immédiat** : Messages d'erreur/succès
4. **Interface réactive** : Rechargement automatique
5. **Code réutilisable** : Fonctions modulaires

---

**Cette partie représente ~120 lignes d'interface avec intégration BDD complète !** 