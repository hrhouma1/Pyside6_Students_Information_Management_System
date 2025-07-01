# Guide Partie 2 : Opérations CRUD - Base de données

## Lignes 45-75 : Fonction d'ajout d'étudiant

```python
def add_student(self, first_name: str, last_name: str, city: str, state: str, email: str) -> bool:
    """
    Add a new student to the database
    
    Args:
        first_name: Student's first name
        last_name: Student's last name
        city: Student's city
        state: Student's state
        email: Student's email address
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = self.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (first_name, last_name, city, state, email)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, city, state, email))
            conn.commit()
            print(f"Étudiant {first_name} {last_name} ajouté avec succès.")
            return True
        except sqlite3.IntegrityError:
            print(f"Erreur: L'email {email} existe déjà dans la base de données.")
            return False
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de l'étudiant: {e}")
            return False
        finally:
            conn.close()
    return False
```

### **Points techniques détaillés :**

#### **Ligne 45 : Signature de la fonction**
```python
def add_student(self, first_name: str, last_name: str, city: str, state: str, email: str) -> bool:
```
- **Type hints** : Chaque paramètre est typé comme `str`
- **Valeur de retour** : `-> bool` indique que la fonction retourne True/False
- **5 paramètres** : correspondent aux 5 colonnes de la table (sauf student_id qui est auto-généré)

#### **Lignes 47-57 : Documentation (docstring)**
```python
"""
Add a new student to the database

Args:
    first_name: Student's first name
    last_name: Student's last name
    city: Student's city
    state: Student's state
    email: Student's email address
    
Returns:
    bool: True if successful, False otherwise
"""
```
- **Format Google Style** : Documentation standard Python
- **Args** : Description de chaque paramètre
- **Returns** : Type et signification de la valeur de retour

#### **Lignes 59-75 : Logique principale**

**Ligne 59** : `conn = self.get_connection()`
- Appel de la méthode définie lignes 14-23
- Retourne une connexion SQLite ou None

**Ligne 60** : `if conn:`
- Vérification que la connexion est valide
- Si None, on passe directement à `return False` (ligne 75)

**Lignes 61-74 : Bloc try-except-finally**

**Ligne 62** : `cursor = conn.cursor()`
- Création d'un curseur pour exécuter les requêtes SQL

**Lignes 63-65** : Requête SQL préparée
```python
cursor.execute("""
    INSERT INTO students (first_name, last_name, city, state, email)
    VALUES (?, ?, ?, ?, ?)
""", (first_name, last_name, city, state, email))
```
- **Requête préparée** avec `?` pour éviter les injections SQL
- **Tuple de paramètres** : `(first_name, last_name, city, state, email)`
- **Colonnes explicites** : on n'insère pas student_id (auto-généré)

**Ligne 66** : `conn.commit()`
- **Validation de la transaction** : rend les changements permanents
- Sans commit, les changements sont perdus

**Ligne 67-68** : Message de succès
```python
print(f"Étudiant {first_name} {last_name} ajouté avec succès.")
return True
```

**Ligne 69-70** : Gestion erreur email dupliqué
```python
except sqlite3.IntegrityError:
    print(f"Erreur: L'email {email} existe déjà dans la base de données.")
```
- **IntegrityError** : Exception spécifique pour violation de contrainte UNIQUE
- **Email dupliqué** : La contrainte UNIQUE sur email déclenche cette erreur

**Ligne 72-73** : Gestion erreur générale
```python
except sqlite3.Error as e:
    print(f"Erreur lors de l'ajout de l'étudiant: {e}")
```

**Ligne 74** : Nettoyage garanti
```python
finally:
    conn.close()
```
- **finally** : S'exécute toujours, même en cas d'erreur
- **Fermeture connexion** : Libère les ressources

---

## Lignes 77-91 : Récupération de tous les étudiants

```python
def get_all_students(self) -> List[Tuple]:
    """
    Retrieve all students from the database
    
    Returns:
        List of tuples containing student data
    """
    conn = self.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            return students
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des étudiants: {e}")
            return []
        finally:
            conn.close()
    return []
```

### **Analyse détaillée :**

**Ligne 77** : `-> List[Tuple]`
- **Type de retour** : Liste de tuples
- **Chaque tuple** : (student_id, first_name, last_name, city, state, email)

**Ligne 87** : `cursor.execute("SELECT * FROM students")`
- **SELECT *** : Récupère toutes les colonnes
- **FROM students** : De la table students
- **Pas de WHERE** : Récupère tous les enregistrements

**Ligne 88** : `students = cursor.fetchall()`
- **fetchall()** : Récupère tous les résultats d'un coup
- **Alternative** : fetchone() pour un résultat, fetchmany(n) pour n résultats

**Ligne 91** : `return []`
- **Liste vide** en cas d'erreur ou de connexion échouée
- **Cohérent** avec le type de retour List[Tuple]

---

## Lignes 93-113 : Récupération par ID

```python
def get_student_by_id(self, student_id: int) -> Optional[Tuple]:
    """
    Retrieve a specific student by ID
    
    Args:
        student_id: The student's ID
        
    Returns:
        Tuple containing student data or None if not found
    """
    conn = self.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()
            return student
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération de l'étudiant: {e}")
            return None
        finally:
            conn.close()
    return None
```

### **Spécificités importantes :**

**Ligne 93** : `-> Optional[Tuple]`
- **Optional[Tuple]** : Équivalent à `Union[Tuple, None]`
- **Peut retourner None** si l'étudiant n'existe pas

**Ligne 106** : `(student_id,)`
- **Tuple à un élément** : La virgule est obligatoire
- **Sans virgule** : `(student_id)` serait juste des parenthèses

**Ligne 107** : `fetchone()`
- **Un seul résultat** : Premier résultat ou None si aucun
- **Adapté pour clé primaire** : student_id est unique

---

## Lignes 115-150 : Mise à jour d'étudiant

```python
def update_student(self, student_id: int, first_name: str, last_name: str, 
                  city: str, state: str, email: str) -> bool:
    """
    Update an existing student's information
    
    Args:
        student_id: The student's ID
        first_name: Updated first name
        last_name: Updated last name
        city: Updated city
        state: Updated state
        email: Updated email address
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = self.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students 
                SET first_name = ?, last_name = ?, city = ?, state = ?, email = ?
                WHERE student_id = ?
            """, (first_name, last_name, city, state, email, student_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"Étudiant ID {student_id} mis à jour avec succès.")
                return True
            else:
                print(f"Aucun étudiant trouvé avec l'ID {student_id}.")
                return False
        except sqlite3.IntegrityError:
            print(f"Erreur: L'email {email} existe déjà dans la base de données.")
            return False
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de l'étudiant: {e}")
            return False
        finally:
            conn.close()
    return False
```

### **Points techniques avancés :**

**Lignes 137-140** : Requête UPDATE
```python
cursor.execute("""
    UPDATE students 
    SET first_name = ?, last_name = ?, city = ?, state = ?, email = ?
    WHERE student_id = ?
""", (first_name, last_name, city, state, email, student_id))
```
- **6 paramètres** : 5 pour SET + 1 pour WHERE
- **Ordre important** : Correspond à l'ordre des ? dans la requête

**Ligne 142** : `cursor.rowcount`
- **Nombre de lignes affectées** par la dernière requête
- **0** : Aucun étudiant trouvé avec cet ID
- **1** : Un étudiant mis à jour (normal)
- **>1** : Impossible avec une clé primaire

**Lignes 143-149** : Logique conditionnelle
- **Si rowcount > 0** : Commit et message de succès
- **Sinon** : Message d'erreur, pas de commit

---

## Lignes 152-175 : Suppression d'étudiant

```python
def delete_student(self, student_id: int) -> bool:
    """
    Delete a student from the database
    
    Args:
        student_id: The student's ID to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = self.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"Étudiant ID {student_id} supprimé avec succès.")
                return True
            else:
                print(f"Aucun étudiant trouvé avec l'ID {student_id}.")
                return False
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de l'étudiant: {e}")
            return False
        finally:
            conn.close()
    return False
```

### **Simplicité et efficacité :**

**Ligne 166** : `DELETE FROM students WHERE student_id = ?`
- **Requête simple** : Une seule condition
- **Sécurisée** : Paramètre préparé

**Même logique rowcount** que pour UPDATE
- **Vérification** que la suppression a eu lieu
- **Commit conditionnel** seulement si succès

---

## Patterns communs identifiés

### 1. **Structure try-except-finally**
Toutes les méthodes utilisent le même pattern :
```python
conn = self.get_connection()
if conn:
    try:
        # Logique SQL
    except sqlite3.Error as e:
        # Gestion erreur
    finally:
        conn.close()
return valeur_par_defaut
```

### 2. **Gestion des erreurs hiérarchique**
```python
except sqlite3.IntegrityError:        # Spécifique
    # Traitement spécialisé
except sqlite3.Error as e:            # Général
    # Traitement générique
```

### 3. **Requêtes préparées systématiques**
```python
cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
```
- **Jamais de concaténation** de strings
- **Toujours des paramètres** avec `?`

### 4. **Validation des résultats**
```python
if cursor.rowcount > 0:
    # Opération réussie
else:
    # Aucun enregistrement affecté
```

### 5. **Messages utilisateur informatifs**
```python
print(f"Étudiant {first_name} {last_name} ajouté avec succès.")
print(f"Erreur: L'email {email} existe déjà dans la base de données.")
```

---

**Cette partie représente ~130 lignes de code CRUD avec gestion d'erreurs complète !** 