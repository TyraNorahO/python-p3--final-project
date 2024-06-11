import sqlite3

CONN = sqlite3.connect('medication_tracker.db')
CURSOR = CONN.cursor()
