import sqlite3

conn = sqlite3.connect('C:/Users/Chua Shi Min/Documents/culinary/data/culinary.db')

cursor = conn.cursor()

result = cursor.execute('SELECT * FROM recipes')
result.fetchone()
print('finish')
