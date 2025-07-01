# 🎓 Guide d'utilisation - Système de Gestion des Informations Étudiantes

## 📋 Table des matières
1. [Installation et Configuration](#installation-et-configuration)
2. [Lancement de l'Application](#lancement-de-lapplication)
3. [Interface Utilisateur](#interface-utilisateur)
4. [Fonctionnalités](#fonctionnalités)
5. [Base de Données](#base-de-données)
6. [Dépannage](#dépannage)

---

## 🚀 Installation et Configuration

### Prérequis
- Python 3.7 ou plus récent
- Windows 10/11 avec PowerShell

### Étapes d'installation

#### 1. Créer l'environnement virtuel
```powershell
python -m venv venv_students
```

#### 2. Activer l'environnement virtuel
```powershell
.\venv_students\Scripts\Activate.ps1
```
> Vous devriez voir `(venv_students)` au début de votre invite de commande

#### 3. Installer PySide6
```powershell
pip install PySide6
```

#### 4. Ajouter des données de test (optionnel)
```powershell
python add_test_data.py
```

---

## 🖥️ Lancement de l'Application

### Méthode recommandée
```powershell
# Activer l'environnement virtuel
.\venv_students\Scripts\Activate.ps1

# Lancer l'application
python main.py
```

### Vérification
- L'interface graphique devrait s'ouvrir
- Le tableau devrait afficher les étudiants existants
- Les ComboBox État/Ville devraient être remplies

---

## 🎨 Interface Utilisateur

### Sections principales

#### 1. **Formulaire de saisie** (Haut)
- **Student ID** : Champ auto-généré (lecture seule)
- **First Name** : Prénom de l'étudiant
- **Last Name** : Nom de famille de l'étudiant
- **Email Address** : Adresse email (unique)
- **State** : Liste déroulante des états
- **City** : Liste déroulante des villes (dépend de l'état)

#### 2. **Boutons d'action** (Milieu)
- **Add** : Ajouter un nouvel étudiant
- **Update** : Modifier l'étudiant sélectionné
- **Select** : Charger les données dans le formulaire
- **Search** : Rechercher des étudiants
- **Clear** : Vider le formulaire
- **Delete** : Supprimer l'étudiant sélectionné

#### 3. **Tableau des résultats** (Bas)
- Affiche tous les étudiants de la base de données
- Colonnes : ID, Prénom, Nom, Ville, État, Email
- Sélection par ligne entière

---

## ⚡ Fonctionnalités

### 📝 Ajouter un étudiant

1. Remplir tous les champs du formulaire
2. Sélectionner un état dans la liste déroulante
3. Sélectionner une ville correspondante
4. Cliquer sur **Add**
5. Un message de confirmation apparaîtra
6. Le tableau se met à jour automatiquement

**Validations :**
- Tous les champs sont obligatoires
- L'email doit contenir '@' et '.'
- L'email doit être unique

### ✏️ Modifier un étudiant

1. Cliquer sur une ligne dans le tableau
2. Cliquer sur **Select** pour charger les données
3. Modifier les champs souhaités
4. Cliquer sur **Update**
5. Confirmer la modification

### 🔍 Rechercher des étudiants

1. Saisir un terme de recherche dans le champ de recherche
2. Cliquer sur **Search**
3. Les résultats s'affichent dans le tableau
4. Pour voir tous les étudiants, laisser vide et rechercher

**La recherche porte sur :**
- Prénom
- Nom de famille
- Ville
- État
- Email

### 🗑️ Supprimer un étudiant

1. Sélectionner une ligne dans le tableau
2. Cliquer sur **Delete**
3. Confirmer la suppression dans la boîte de dialogue
4. L'étudiant est supprimé définitivement

### 🧹 Vider le formulaire

- Cliquer sur **Clear** pour vider tous les champs

---

## 💾 Base de Données

### Structure
La base de données SQLite (`students.db`) contient une table `students` :

| Colonne    | Type    | Description                    |
|------------|---------|--------------------------------|
| student_id | INTEGER | Clé primaire auto-incrémentée  |
| first_name | TEXT    | Prénom (obligatoire)           |
| last_name  | TEXT    | Nom de famille (obligatoire)   |
| city       | TEXT    | Ville (obligatoire)            |
| state      | TEXT    | État (obligatoire)             |
| email      | TEXT    | Email unique (obligatoire)     |

### Fichiers de base de données
- **students.db** : Base de données principale
- **connect_database.py** : Module de gestion de la BDD
- **add_test_data.py** : Script d'ajout de données de test

### Sauvegarde
Pour sauvegarder vos données, copiez le fichier `students.db`

---

## 🔧 Dépannage

### Problèmes courants

#### L'application ne se lance pas
```powershell
# Vérifier que l'environnement virtuel est activé
.\venv_students\Scripts\Activate.ps1

# Vérifier l'installation de PySide6
pip list | findstr PySide6

# Réinstaller si nécessaire
pip install --upgrade PySide6
```

#### Erreur "Module not found"
```powershell
# S'assurer d'être dans le bon répertoire
cd C:\projetspyside6\Pyside6_Students_Information_Management_System

# Vérifier les fichiers
dir *.py
```

#### Base de données corrompue
```powershell
# Supprimer et recréer la base
del students.db
python connect_database.py
python add_test_data.py
```

#### Interface ne répond pas
- Fermer l'application avec Ctrl+C dans le terminal
- Relancer avec `python main.py`

### Messages d'erreur courants

| Erreur | Solution |
|--------|----------|
| "Tous les champs sont obligatoires!" | Remplir tous les champs du formulaire |
| "Format d'email invalide!" | Utiliser un format email valide (ex: nom@domain.com) |
| "L'email existe déjà" | Utiliser une adresse email différente |
| "Veuillez sélectionner un étudiant" | Cliquer sur une ligne du tableau |

---

## 📊 Données de test

Le script `add_test_data.py` ajoute 10 étudiants de test :

1. Marie Martin (Paris, Île-de-France)
2. Pierre Dupont (Lyon, Auvergne-Rhône-Alpes)
3. Sophie Bernard (Marseille, Provence-Alpes-Côte d'Azur)
4. Thomas Dubois (Toulouse, Occitanie)
5. Emma Moreau (Nice, Provence-Alpes-Côte d'Azur)
6. Lucas Simon (Nantes, Pays de la Loire)
7. Camille Michel (Strasbourg, Grand Est)
8. Julien Leroy (Bordeaux, Nouvelle-Aquitaine)
9. Clara Roux (Lille, Hauts-de-France)
10. Antoine David (Rennes, Bretagne)

---

## 🎯 Conseils d'utilisation

### Bonnes pratiques
- Toujours activer l'environnement virtuel avant utilisation
- Faire des sauvegardes régulières du fichier `students.db`
- Tester les fonctionnalités avec les données de test
- Utiliser des emails uniques pour chaque étudiant

### Raccourcis
- **Double-clic** sur une ligne : équivalent à Select
- **Ctrl+C** dans le terminal : arrêter l'application
- **F5** ou redémarrage : actualiser les données

---

## 📞 Support

En cas de problème persistant :
1. Vérifier que tous les fichiers sont présents
2. S'assurer que Python et PySide6 sont correctement installés
3. Consulter les messages d'erreur dans le terminal
4. Redémarrer l'application

---

**Version** : 1.0  
**Dernière mise à jour** : [Date actuelle]  
**Auteur** : Système de Gestion des Informations Étudiantes 