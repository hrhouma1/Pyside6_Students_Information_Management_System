from connect_database import DatabaseManager

def add_canadian_test_data():
    """Ajouter des données de test canadiennes dans la base MySQL"""
    
    db = DatabaseManager()
    
    # Données de test canadiennes
    canadian_students = [
        ("Marie", "Tremblay", "Montréal", "Québec", "marie.tremblay@email.com"),
        ("Jean", "Bouchard", "Québec", "Québec", "jean.bouchard@email.com"),
        ("Sarah", "Smith", "Toronto", "Ontario", "sarah.smith@email.com"),
        ("Michael", "Johnson", "Ottawa", "Ontario", "michael.johnson@email.com"),
        ("Emily", "Wilson", "Vancouver", "Colombie-Britannique", "emily.wilson@email.com"),
        ("David", "Brown", "Calgary", "Alberta", "david.brown@email.com"),
        ("Jessica", "Taylor", "Edmonton", "Alberta", "jessica.taylor@email.com"),
        ("Robert", "Anderson", "Winnipeg", "Manitoba", "robert.anderson@email.com"),
        ("Ashley", "Thomas", "Halifax", "Nouvelle-Écosse", "ashley.thomas@email.com"),
        ("Christopher", "Martin", "Saskatoon", "Saskatchewan", "christopher.martin@email.com"),
        ("Amanda", "White", "Victoria", "Colombie-Britannique", "amanda.white@email.com"),
        ("Daniel", "Garcia", "Moncton", "Nouveau-Brunswick", "daniel.garcia@email.com")
    ]
    
    successful_additions = 0
    total_students = len(canadian_students)
    
    print("=== Ajout d'étudiants canadiens dans MySQL ===")
    print()
    
    for first_name, last_name, city, state, email in canadian_students:
        success = db.add_student(first_name, last_name, city, state, email)
        if success:
            successful_additions += 1
            print(f"✓ {first_name} {last_name} - {city}, {state}")
        else:
            print(f"✗ Échec pour {first_name} {last_name}")
    
    print()
    print(f"=== Résumé ===")
    print(f"Étudiants ajoutés avec succès: {successful_additions}/{total_students}")
    
    # Vérifier le total d'étudiants dans la base
    total_in_db = db.get_student_count()
    print(f"Total d'étudiants dans la base MySQL: {total_in_db}")
    
    print()
    print("=== Vérification des provinces ===")
    states = db.get_states()
    print(f"Provinces trouvées: {', '.join(states)}")
    
    print()
    print("=== Test terminé ===")
    print("Vous pouvez maintenant utiliser l'application PySide6 !")

if __name__ == "__main__":
    add_canadian_test_data() 