# lib/cli.py
import sqlite3
import datetime
from models.reminder import ReminderManager
from models.schedule import ScheduleManager
from models.medication_tracker import MedicationTrackerDB

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
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminder (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               medication_id INTEGER,
                               time TEXT NOT NULL,
                               message TEXT,
                               FOREIGN KEY (medication_id) REFERENCES medication(id)
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

    def update_medication(self, med_id, name=None, dosage=None):
        if name:
            self.cursor.execute('UPDATE medication SET Name = ? WHERE id = ?', (name, med_id))
        if dosage:
            self.cursor.execute('UPDATE medication SET Dosage = ? WHERE id = ?', (dosage, med_id))
        self.connection.commit()
        print(f"Updated medication ID: {med_id}")

    def find_medication(self, name=None, user_id=None):
        if name and user_id:
            self.cursor.execute('SELECT * FROM medication WHERE Name = ? AND user_id = ?', (name, user_id))
        elif name:
            self.cursor.execute('SELECT * FROM medication WHERE Name = ?', (name,))
        elif user_id:
            self.cursor.execute('SELECT * FROM medication WHERE user_id = ?', (user_id,))
        medications = self.cursor.fetchall()
        for med in medications:
            print(f"Medication ID: {med[0]}, Name: {med[1]}, Dosage: {med[2]}, User ID: {med[3]}")
        return medications

    def delete_medication(self, med_id):
        self.cursor.execute('DELETE FROM medication WHERE id = ?', (med_id,))
        self.connection.commit()
        print(f"Deleted medication with ID: {med_id}")

    def close(self):
        self.connection.close()

class ScheduleManager:
    def __init__(self):
        self.connection = sqlite3.connect('medicationtracker.db')
        self.cursor = self.connection.cursor()

    def add_schedule(self, user_id, time):
        try:
            parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            self.cursor.execute('INSERT INTO schedule (user_id, time) VALUES (?, ?)', 
                                (user_id, parsed_time))
            self.connection.commit()
            print(f"Added schedule for User ID: {user_id} at {parsed_time}")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")

    def update_schedule(self, schedule_id, time):
        try:
            parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            self.cursor.execute('UPDATE schedule SET time = ? WHERE id = ?', 
                                (parsed_time, schedule_id))
            self.connection.commit()
            print(f"Updated schedule ID: {schedule_id} to {parsed_time}")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")

    def find_schedule(self, user_id=None, start_time=None, end_time=None):
        if user_id:
            self.cursor.execute('SELECT * FROM schedule WHERE user_id = ?', (user_id,))
        elif start_time and end_time:
            start_parsed = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            end_parsed = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            self.cursor.execute('SELECT * FROM schedule WHERE time BETWEEN ? AND ?', 
                                (start_parsed, end_parsed))
        schedules = self.cursor.fetchall()
        for sched in schedules:
            print(f"Schedule ID: {sched[0]}, User ID: {sched[1]}, Time: {sched[2]}")
        return schedules

    def delete_schedule(self, schedule_id):
        self.cursor.execute('DELETE FROM schedule WHERE id = ?', (schedule_id,))
        self.connection.commit()
        print(f"Deleted schedule with ID: {schedule_id}")

    def view_schedules(self):
        self.cursor.execute('SELECT * FROM schedule')
        schedules = self.cursor.fetchall()
        for sched in schedules:
            print(f"Schedule ID: {sched[0]}, User ID: {sched[1]}, Time: {sched[2]}")

    def close(self):
        self.connection.close()

    def add_reminder(self, medication_id, time, message):
        try:
            parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            self.cursor.execute('INSERT INTO reminder (medication_id, time, message) VALUES (?, ?, ?)', 
                                (medication_id, parsed_time, message))
            self.connection.commit()
            print(f"Added reminder for Medication ID: {medication_id} at {parsed_time} with message: '{message}'")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")

    def update_reminder(self, reminder_id, time=None, message=None):
        try:
            if time:
                parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
                self.cursor.execute('UPDATE reminder SET time = ? WHERE id = ?', 
                                    (parsed_time, reminder_id))
            if message:
                self.cursor.execute('UPDATE reminder SET message = ? WHERE id = ?', 
                                    (message, reminder_id))
            self.connection.commit()
            print(f"Updated reminder ID: {reminder_id}")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")

    def find_reminder(self, medication_id=None, time=None):
        if medication_id and time:
            parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            self.cursor.execute('SELECT * FROM reminder WHERE medication_id = ? AND time = ?', 
                                (medication_id, parsed_time))
        elif medication_id:
            self.cursor.execute('SELECT * FROM reminder WHERE medication_id = ?', 
                                (medication_id,))
        elif time:
            parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            self.cursor.execute('SELECT * FROM reminder WHERE time = ?', 
                                (parsed_time,))
        reminders = self.cursor.fetchall()
        for reminder in reminders:
            print(f"Reminder ID: {reminder[0]}, Medication ID: {reminder[1]}, Time: {reminder[2]}, Message: {reminder[3]}")
        return reminders

    def delete_reminder(self, reminder_id):
        self.cursor.execute('DELETE FROM reminder WHERE id = ?', (reminder_id,))
        self.connection.commit()
        print(f"Deleted reminder with ID: {reminder_id}")

    def view_reminders(self):
        self.cursor.execute('SELECT * FROM reminder')
        reminders = self.cursor.fetchall()
        for reminder in reminders:
            print(f"Reminder ID: {reminder[0]}, Medication ID: {reminder[1]}, Time: {reminder[2]}, Message: {reminder[3]}")

    def close(self):
        self.connection.close()

def main():
    db = MedicationTrackerDB()
    reminder_manager = ReminderManager()
    schedule_manager = ScheduleManager()

    while True:
        menu()
        choice = input("> ")
        
        if choice == "0":
            db.close()
            reminder_manager.close()
            schedule_manager.close()
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
            schedule_manager.add_schedule(user_id, time)
        elif choice == "3":
            med_id = int(input("Enter medication ID to delete: "))
            db.delete_medication(med_id)
        elif choice == "4":
            schedule_id = int(input("Enter schedule ID to delete: "))
            schedule_manager.delete_schedule(schedule_id)
        elif choice == "5":
            db.view_medication()
        elif choice == "6":
            reminder_manager.view_reminders()
        elif choice == "7":
            medication_id = int(input("Enter medication ID: "))
            reminder_time = input("Enter reminder time (YYYY-MM-DD HH:MM): ")
            message = input("Enter reminder message: ")
            reminder_manager.add_reminder(medication_id, reminder_time, message)
        elif choice == "8":
            reminder_id = int(input("Enter reminder ID to delete: "))
            reminder_manager.delete_reminder(reminder_id)
        elif choice == "9":
            schedule_manager.view_schedules()
        elif choice == "10":
            med_id = int(input("Enter medication ID to update: "))
            name = input("Enter new name (or press enter to skip): ")
            dosage = input("Enter new dosage (or press enter to skip): ")
            db.update_medication(med_id, name or None, dosage or None)
        elif choice == "11":
            name = input("Enter medication name to find (or press enter to skip): ")
            user_id = input("Enter user ID to find medications for (or press enter to skip): ")
            db.find_medication(name or None, int(user_id) if user_id else None)
        elif choice == "12":
            schedule_id = int(input("Enter schedule ID to update: "))
            time = input("Enter new schedule time (YYYY-MM-DD HH:MM): ")
            schedule_manager.update_schedule(schedule_id, time)
        elif choice == "13":
            user_id = input("Enter user ID to find schedules for (or press enter to skip): ")
            start_time = input("Enter start time (YYYY-MM-DD HH:MM) to find schedules (or press enter to skip): ")
            end_time = input("Enter end time (YYYY-MM-DD HH:MM) to find schedules (or press enter to skip): ")
            schedule_manager.find_schedule(user_id=int(user_id) if user_id else None, 
                                           start_time=start_time or None, 
                                           end_time=end_time or None)
        elif choice == "14":
            reminder_id = int(input("Enter reminder ID to update: "))
            time = input("Enter new reminder time (YYYY-MM-DD HH:MM): ")
            message = input("Enter new reminder message: ")
            reminder_manager.update_reminder(reminder_id, time or None, message or None)
        elif choice == "15":
            medication_id = input("Enter medication ID to find reminders for (or press enter to skip): ")
            time = input("Enter reminder time (YYYY-MM-DD HH:MM) to find reminders (or press enter to skip): ")
            reminder_manager.find_reminder(medication_id=int(medication_id) if medication_id else None, 
                                           time=time or None)
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
    print("6. View all reminders")
    print("7. Add reminder")
    print("8. Delete reminder")
    print("9. View all schedules")
    print("10. Update medication")
    print("11. Find medication")
    print("12. Update schedule")
    print("13. Find schedule")
    print("14. Update reminder")
    print("15. Find reminder")

if __name__ == "__main__":
    main()    