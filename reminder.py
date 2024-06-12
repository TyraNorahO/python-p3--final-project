import sqlite3
import datetime

class ReminderManager:
    def __init__(self):
        self.connection = sqlite3.connect('medicationtracker.db')
        self.cursor = self.connection.cursor()
        self.create_reminder_table()

    def create_reminder_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reminder (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                medication_id INTEGER,
                                reminder_time TEXT NOT NULL,
                                message TEXT,
                                FOREIGN KEY (medication_id) REFERENCES medication(id)
                              )''')
        self.connection.commit()

    def add_reminder(self, medication_id, reminder_time, message):
        try:
            parsed_time = datetime.datetime.strptime(reminder_time, '%Y-%m-%d %H:%M')
            self.cursor.execute('INSERT INTO reminder (medication_id, reminder_time, message) VALUES (?, ?, ?)',
                                (medication_id, parsed_time, message))
            self.connection.commit()
            print(f"Added reminder for Medication ID: {medication_id} at {parsed_time} with message: {message}")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def view_reminders(self):
        self.cursor.execute('SELECT * FROM reminder')
        reminders = self.cursor.fetchall()
        if reminders:
            for rem in reminders:
                print(f"Reminder ID: {rem[0]}, Medication ID: {rem[1]}, Time: {rem[2]}, Message: {rem[3]}")
        else:
            print("No reminders found.")

    def delete_reminder(self, reminder_id):
        try:
            self.cursor.execute('DELETE FROM reminder WHERE id = ?', (reminder_id,))
            self.connection.commit()
            print(f"Deleted reminder with ID: {reminder_id}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    manager = ReminderManager()
    # Example usage
    manager.add_reminder(1, '2024-12-25 09:00', 'Take your morning medication.')
    manager.view_reminders()
    manager.delete_reminder(1)
    manager.view_reminders()
    manager.close()
