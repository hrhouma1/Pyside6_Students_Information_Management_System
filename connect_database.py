import sqlite3
import os
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "students.db"):
        """
        Initialize database connection and create tables if they don't exist
        """
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self):
        """
        Create and return a database connection
        """
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return None
    
    def create_tables(self):
        """
        Create the students table if it doesn't exist
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        city TEXT NOT NULL,
                        state TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE
                    )
                """)
                conn.commit()
                print("Table 'students' créée avec succès.")
            except sqlite3.Error as e:
                print(f"Erreur lors de la création de la table: {e}")
            finally:
                conn.close()
    
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
    
    def search_students(self, search_term: str, search_field: str = "all") -> List[Tuple]:
        """
        Search for students based on a search term and field
        
        Args:
            search_term: The term to search for
            search_field: The field to search in ('all', 'first_name', 'last_name', 'city', 'state', 'email')
            
        Returns:
            List of tuples containing matching student data
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                search_term = f"%{search_term}%"
                
                if search_field == "all":
                    cursor.execute("""
                        SELECT * FROM students 
                        WHERE first_name LIKE ? OR last_name LIKE ? OR 
                              city LIKE ? OR state LIKE ? OR email LIKE ?
                    """, (search_term, search_term, search_term, search_term, search_term))
                elif search_field in ["first_name", "last_name", "city", "state", "email"]:
                    query = f"SELECT * FROM students WHERE {search_field} LIKE ?"
                    cursor.execute(query, (search_term,))
                else:
                    return []
                
                students = cursor.fetchall()
                return students
            except sqlite3.Error as e:
                print(f"Erreur lors de la recherche: {e}")
                return []
            finally:
                conn.close()
        return []
    
    def get_states(self) -> List[str]:
        """
        Get all unique states from the database
        
        Returns:
            List of unique state names
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT state FROM students ORDER BY state")
                states = [row[0] for row in cursor.fetchall()]
                return states
            except sqlite3.Error as e:
                print(f"Erreur lors de la récupération des états: {e}")
                return []
            finally:
                conn.close()
        return []
    
    def get_cities_by_state(self, state: str) -> List[str]:
        """
        Get all cities for a specific state
        
        Args:
            state: The state name
            
        Returns:
            List of city names for the given state
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT city FROM students WHERE state = ? ORDER BY city", (state,))
                cities = [row[0] for row in cursor.fetchall()]
                return cities
            except sqlite3.Error as e:
                print(f"Erreur lors de la récupération des villes: {e}")
                return []
            finally:
                conn.close()
        return []
    
    def clear_all_students(self) -> bool:
        """
        Clear all students from the database
        
        Returns:
            bool: True if successful, False otherwise
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students")
                conn.commit()
                print("Tous les étudiants ont été supprimés de la base de données.")
                return True
            except sqlite3.Error as e:
                print(f"Erreur lors de la suppression de tous les étudiants: {e}")
                return False
            finally:
                conn.close()
        return False
    
    def get_student_count(self) -> int:
        """
        Get the total number of students in the database
        
        Returns:
            int: Number of students
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM students")
                count = cursor.fetchone()[0]
                return count
            except sqlite3.Error as e:
                print(f"Erreur lors du comptage des étudiants: {e}")
                return 0
            finally:
                conn.close()
        return 0

# Fonction utilitaire pour créer une instance de la base de données
def get_database_manager():
    """
    Create and return a DatabaseManager instance
    """
    return DatabaseManager()

# Test de la base de données (peut être commenté en production)
if __name__ == "__main__":
    # Test des fonctionnalités de base
    db = DatabaseManager()
    
    # Test d'ajout d'un étudiant
    success = db.add_student("Jean", "Dupont", "Paris", "Île-de-France", "jean.dupont@email.com")
    if success:
        print("Test d'ajout réussi")
    
    # Test de récupération de tous les étudiants
    students = db.get_all_students()
    print(f"Nombre d'étudiants: {len(students)}")
    
    # Affichage des étudiants
    for student in students:
        print(f"ID: {student[0]}, Nom: {student[1]} {student[2]}, Ville: {student[3]}, État: {student[4]}, Email: {student[5]}") 