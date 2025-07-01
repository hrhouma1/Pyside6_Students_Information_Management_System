import mysql.connector
from mysql.connector import Error
import os
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "root", database: str = "db_students"):
        """
        Initialize database connection and create tables if they don't exist
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.create_tables()
    
    def get_connection(self):
        """
        Create and return a database connection
        """
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except Error as e:
            print(f"Erreur de connexion à la base de données MySQL: {e}")
            return None
    
    def create_tables(self):
        """
        Create the students_info table with the exact schema from SQL Workbench
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Drop table if exists to recreate with correct schema
                cursor.execute("DROP TABLE IF EXISTS students_info")
                
                # Create table with your exact SQL schema
                cursor.execute("""
                    CREATE TABLE students_info (
                        studentId INT NOT NULL AUTO_INCREMENT,
                        firstName VARCHAR(45) NOT NULL,
                        lastName VARCHAR(45),
                        state VARCHAR(45),
                        city VARCHAR(45),
                        emailAddress VARCHAR(45),
                        PRIMARY KEY (studentId),
                        UNIQUE INDEX studentId_UNIQUE (studentId ASC) VISIBLE
                    )
                """)
                conn.commit()
                print("Table 'students_info' créée avec succès.")
            except Error as e:
                print(f"Erreur lors de la création de la table: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
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
                    INSERT INTO students_info (firstName, lastName, city, state, emailAddress)
                    VALUES (%s, %s, %s, %s, %s)
                """, (first_name, last_name, city, state, email))
                conn.commit()
                print(f"Étudiant {first_name} {last_name} ajouté avec succès.")
                return True
            except mysql.connector.IntegrityError:
                print(f"Erreur: L'email {email} existe déjà dans la base de données.")
                return False
            except Error as e:
                print(f"Erreur lors de l'ajout de l'étudiant: {e}")
                return False
            finally:
                if conn.is_connected():
                    cursor.close()
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
                cursor.execute("SELECT * FROM students_info ORDER BY studentId")
                students = cursor.fetchall()
                return students
            except Error as e:
                print(f"Erreur lors de la récupération des étudiants: {e}")
                return []
            finally:
                if conn.is_connected():
                    cursor.close()
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
                cursor.execute("SELECT * FROM students_info WHERE studentId = %s", (student_id,))
                student = cursor.fetchone()
                return student
            except Error as e:
                print(f"Erreur lors de la récupération de l'étudiant: {e}")
                return None
            finally:
                if conn.is_connected():
                    cursor.close()
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
                    UPDATE students_info 
                    SET firstName = %s, lastName = %s, city = %s, state = %s, emailAddress = %s
                    WHERE studentId = %s
                """, (first_name, last_name, city, state, email, student_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"Étudiant ID {student_id} mis à jour avec succès.")
                    return True
                else:
                    print(f"Aucun étudiant trouvé avec l'ID {student_id}.")
                    return False
            except mysql.connector.IntegrityError:
                print(f"Erreur: L'email {email} existe déjà dans la base de données.")
                return False
            except Error as e:
                print(f"Erreur lors de la mise à jour de l'étudiant: {e}")
                return False
            finally:
                if conn.is_connected():
                    cursor.close()
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
                cursor.execute("DELETE FROM students_info WHERE studentId = %s", (student_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"Étudiant ID {student_id} supprimé avec succès.")
                    return True
                else:
                    print(f"Aucun étudiant trouvé avec l'ID {student_id}.")
                    return False
            except Error as e:
                print(f"Erreur lors de la suppression de l'étudiant: {e}")
                return False
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return False
    
    def search_students(self, search_term: str, search_field: str = "all") -> List[Tuple]:
        """
        Search for students based on a search term and field
        
        Args:
            search_term: The term to search for
            search_field: The field to search in ('all', 'firstName', 'lastName', 'city', 'state', 'emailAddress')
            
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
                        SELECT * FROM students_info 
                        WHERE firstName LIKE %s OR lastName LIKE %s OR 
                              city LIKE %s OR state LIKE %s OR emailAddress LIKE %s
                        ORDER BY studentId
                    """, (search_term, search_term, search_term, search_term, search_term))
                elif search_field in ["firstName", "lastName", "city", "state", "emailAddress"]:
                    query = f"SELECT * FROM students_info WHERE {search_field} LIKE %s ORDER BY studentId"
                    cursor.execute(query, (search_term,))
                else:
                    return []
                
                students = cursor.fetchall()
                return students
            except Error as e:
                print(f"Erreur lors de la recherche: {e}")
                return []
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return []
    
    def get_states(self) -> List[str]:
        """
        Get all unique states from the database
        
        Returns:
            List of state names
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT state FROM students_info WHERE state IS NOT NULL ORDER BY state")
                states = [row[0] for row in cursor.fetchall()]
                return states
            except Error as e:
                print(f"Erreur lors de la récupération des états: {e}")
                return []
            finally:
                if conn.is_connected():
                    cursor.close()
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
                cursor.execute("SELECT DISTINCT city FROM students_info WHERE state = %s AND city IS NOT NULL ORDER BY city", (state,))
                cities = [row[0] for row in cursor.fetchall()]
                return cities
            except Error as e:
                print(f"Erreur lors de la récupération des villes: {e}")
                return []
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return []
    
    def clear_all_students(self) -> bool:
        """
        Delete all students from the database
        
        Returns:
            bool: True if successful, False otherwise
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students_info")
                conn.commit()
                print(f"{cursor.rowcount} étudiants supprimés.")
                return True
            except Error as e:
                print(f"Erreur lors de la suppression des étudiants: {e}")
                return False
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return False
    
    def get_student_count(self) -> int:
        """
        Get the total number of students in the database
        
        Returns:
            Number of students
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM students_info")
                count = cursor.fetchone()[0]
                return count
            except Error as e:
                print(f"Erreur lors du comptage des étudiants: {e}")
                return 0
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        return 0

# Test de la connexion si le fichier est exécuté directement
if __name__ == "__main__":
    db = DatabaseManager()
    
    # Test d'ajout
    success = db.add_student("Jean", "Dupont", "Paris", "Île-de-France", "jean.dupont@email.com")
    if success:
        print("Test d'ajout réussi")
    
    # Test de récupération
    students = db.get_all_students()
    print(f"Nombre d'étudiants: {len(students)}")
    
    for student in students:
        print(f"ID: {student[0]}, Nom: {student[1]} {student[2]}, Ville: {student[3]}, État: {student[4]}, Email: {student[5]}") 