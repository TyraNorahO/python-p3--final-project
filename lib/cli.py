# lib/cli.py
import sqlite3
import datetime
from schedule import ScheduleManager  # Import the ScheduleManager class


def create_tables():
    connection = sqlite3.connect("medicationtracker.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      Name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS medication (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      Name TEXT NOT NULL,
                      Dosage TEXT NOT NULL,
                      user_id INTEGER,
                      FOREIGN KEY (user_id) REFERENCES user(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS schedule (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      time TEXT NOT NULL,
                      FOREIGN KEY (user_id) REFERENCES user(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS dosage_history (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      medication_id INTEGER,
                      time_taken TEXT NOT NULL,
                      FOREIGN KEY (user_id) REFERENCES user(id),
                      FOREIGN KEY (medication_id) REFERENCES medication(id)
    )''')

    connection.commit()
    connection.close()


create_tables()


class MedicationTrackerDB:
    def __init__(self):
        self.connection = sqlite3.connect('medicationtracker.db')
        self.cursor = self.connection.cursor()

    def add_user(self, name):
        self.cursor.execute('INSERT INTO user (Name) VALUES (?)', (name,))
        self.connection.commit()
        print(f"Added user: {name}")

    def view_users(self):
        self.cursor.execute('SELECT * FROM user')
        users = self.cursor.fetchall()
        for user in users:
            print(f"User ID: {user[0]}, Name: {user[1]}")

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM user WHERE id = ?', (user_id,))
        self.connection.commit()
        print(f"Deleted user with ID: {user_id}")

    def add_medication(self, user_id, name, dosage):
        self.cursor.execute('INSERT INTO medication (user_id, Name, Dosage) VALUES (?, ?, ?)', 
                            (user_id, name, dosage))
        self.connection.commit()
        print(f"Added medication: {name}, Dosage: {dosage} for User ID: {user_id}")

    def update_medication(self, med_id, name, dosage):
        self.cursor.execute('UPDATE medication SET Name = ?, Dosage = ? WHERE id = ?', 
                            (name, dosage, med_id))
        self.connection.commit()
        print(f"Updated medication ID: {med_id} to Name: {name}, Dosage: {dosage}")

    def view_medication(self):
        self.cursor.execute('SELECT * FROM medication')
        medications = self.cursor.fetchall()
        for med in medications:
            print(f"Medication ID: {med[0]}, Name: {med[1]}, Dosage: {med[2]}, User ID: {med[3]}")
    
    def delete_medication(self, med_id):
        self.cursor.execute('DELETE FROM medication WHERE id = ?', (med_id,))
        self.connection.commit()
        print(f"Deleted medication with ID: {med_id}")

    def record_dosage(self, user_id, medication_id):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO dosage_history (user_id, medication_id, time_taken) VALUES (?, ?, ?)', 
                            (user_id, medication_id, current_time))
        self.connection.commit()
        print(f"Recorded dosage for medication ID: {medication_id} for User ID: {user_id} at {current_time}")

    def view_dosage_history(self):
        self.cursor.execute('SELECT * FROM dosage_history')
        history = self.cursor.fetchall()
        for entry in history:
            print(f"Entry ID: {entry[0]}, User ID: {entry[1]}, Medication ID: {entry[2]}, Time Taken: {entry[3]}")

    def close(self):
        self.connection.close()


def main():
    db = MedicationTrackerDB()
    schedule_manager = ScheduleManager()  # Create an instance of ScheduleManager
    
    while True:
        menu()
        choice = input("> ")
        
        if choice == "0":
            db.close()
            schedule_manager.close()  # Close the ScheduleManager
            print("Exiting the program.")
            break
        elif choice == "1":
            name = input("Enter user name: ")
            db.add_user(name)
        elif choice == "2":
            user_id = int(input("Enter user ID: "))
            name = input("Enter medication name: ")
            dosage = input("Enter dosage: ")
            db.add_medication(user_id, name, dosage)
        elif choice == "3":
            med_id = int(input("Enter medication ID to update: "))
            name = input("Enter new medication name: ")
            dosage = input("Enter new dosage: ")
            db.update_medication(med_id, name, dosage)
        elif choice == "4":
            user_id = int(input("Enter user ID: "))
            time = input("Enter schedule time (YYYY-MM-DD HH:MM): ")
            schedule_manager.add_schedule(user_id, time)
        elif choice == "5":
            med_id = int(input("Enter medication ID to delete: "))
            db.delete_medication(med_id)
        elif choice == "6":
            schedule_id = int(input("Enter schedule ID to delete: "))
            schedule_manager.delete_schedule(schedule_id)
        elif choice == "7":
            db.view_users()
        elif choice == "8":
            db.view_medication()
        elif choice == "9":
            schedule_manager.view_schedules()
        elif choice == "10":
            user_id = int(input("Enter user ID: "))
            medication_id = int(input("Enter medication ID: "))
            db.record_dosage(user_id, medication_id)
        elif choice == "11":
            db.view_dosage_history()
        else:
            print("Invalid choice. Please try again.")


def menu():
    print("\nPlease select an option:")
    print("0. Exit the program")
    print("1. Add user")
    print("2. Add medication")
    print("3. Update medication")
    print("4. Add schedule")
    print("5. Delete medication")
    print("6. Delete schedule")
    print("7. View all users")
    print("8. View all medications")
    print("9. View all schedules")
    print("10. Record medication dosage")
    print("11. View dosage history")


if __name__ == "__main__":
    main()
