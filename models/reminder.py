import sqlite3
import datetime

class ReminderManager:
    def __init__(self):
        self.connection = sqlite3.connect('medicationtracker.db')
        self.cursor = self.connection.cursor()
      
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

    def update_reminder(self, reminder_id, new_time=None, new_message=None):
        try:
            updates = []
            parameters = []
            
            if new_time:
                parsed_time = datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M')
                updates.append("reminder_time = ?")
                parameters.append(parsed_time)

            if new_message:
                updates.append("message = ?")
                parameters.append(new_message)

            if updates:
                parameters.append(reminder_id)
                query = f'UPDATE reminder SET {", ".join(updates)} WHERE id = ?'
                self.cursor.execute(query, parameters)
                self.connection.commit()
                print(f"Updated reminder ID: {reminder_id}")
            else:
                print("No updates provided.")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def find_reminder(self, medication_id=None, time=None):
        try:
            query = 'SELECT * FROM reminder WHERE'
            conditions = []
            parameters = []

            if medication_id is not None:
                conditions.append("medication_id = ?")
                parameters.append(medication_id)

            if time is not None:
                parsed_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
                conditions.append("reminder_time = ?")
                parameters.append(parsed_time)

            if conditions:
                query += ' AND '.join(conditions)
                self.cursor.execute(query, parameters)
                reminders = self.cursor.fetchall()
                if reminders:
                    for rem in reminders:
                        print(f"Reminder ID: {rem[0]}, Medication ID: {rem[1]}, Time: {rem[2]}, Message: {rem[3]}")
                else:
                    print("No reminders found with the given criteria.")
            else:
                print("Please provide at least one search criterion: medication_id or time.")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD HH:MM'")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    manager = ReminderManager()
    # Example usage
    manager.add_reminder(1, '2024-12-25 09:00', 'Take your morning medication.')
    manager.view_reminders()
    manager.update_reminder(1, new_time='2024-12-25 10:00', new_message='Take your updated medication.')
    manager.find_reminder(medication_id=1)
    manager.delete_reminder(1)
    manager.view_reminders()
    manager.close()
