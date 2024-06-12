# lib/cli.py
import sqlite3
import datetime


def create_tables():
    connection = sqlite3.connect("medicationtracker.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
        create_tables()              Name TEXT NOT NULL
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

    connection.commit()
    connection.close()


create_tables()


class MedicationTrackerDB:
    def __init__(self):
        self.connection = sqlite3.connect('medicationtracker.db')
        self.cursor = self.connection.cursor()

    def add_medication(self, user_id, name, dosage):
        self.cursor.execute('INSERT INTO medication (user_id, Name, Dosage) VALUES (?, ?, ?)', 
                            (user_id, name, dosage))
        self.connection.commit()
        print(f"Added medication: {name}, Dosage: {dosage} for User ID: {user_id}")

    def view_medication(self):
        self.cursor.execute('SELECT * FROM medication')
        medications = self.cursor.fetchall()
        for med in medications:
            print(f"Medication ID: {med[0]}, Name: {med[1]}, Dosage: {med[2]}, User ID: {med[3]}")
    
    def add_schedule(self, user_id, time):
        try:
            parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            self.cursor.execute('INSERT INTO schedule (user_id, time) VALUES (?, ?)', 
                                (user_id, parsed_time))
            self.connection.commit()
            print(f"Added schedule for User ID: {user_id} at {parsed_time}")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")

    def delete_medication(self, med_id):
        self.cursor.execute('DELETE FROM medication WHERE id = ?', (med_id,))
        self.connection.commit()
        print(f"Deleted medication with ID: {med_id}")

    def delete_schedule(self, schedule_id):
        self.cursor.execute('DELETE FROM schedule WHERE id = ?', (schedule_id,))
        self.connection.commit()
        print(f"Deleted schedule with ID: {schedule_id}")

    def close(self):
        self.connection.close()

def main():
    db = MedicationTrackerDB()
    
    while True:
        menu()
        choice = input("> ")
        
        if choice == "0":
            db.close()
            print("Exiting the program.")
            break
        elif choice == "1":
            user_id = int(input("Enter user ID: "))
            name = input("Enter medication name: ")
            dosage = input("Enter dosage: ")
            db.add_medication(user_id, name, dosage)
        elif choice == "2":
            user_id = int(input("Enter user ID: "))
            time = input("Enter schedule time (YYYY-MM-DD HH:MM): ")
            db.add_schedule(user_id, time)
        elif choice == "3":
            med_id = int(input("Enter medication ID to delete: "))
            db.delete_medication(med_id)
        elif choice == "4":
            schedule_id = int(input("Enter schedule ID to delete: "))
            db.delete_schedule(schedule_id)
        elif choice == "5":
            db.view_medication()
        else:
            print("Invalid choice. Please try again.")

def menu():
    print("\nPlease select an option:")
    print("0. Exit the program")
    print("1. Add medication")
    print("2. Add schedule")
    print("3. Delete medication")
    print("4. Delete schedule")
    print("5. View all medications")

if __name__ == "__main__":
    main()
