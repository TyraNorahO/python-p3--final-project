# lib/cli.py
import sqlite3
import datetime

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

    def close(self):
        self.connection.close()
