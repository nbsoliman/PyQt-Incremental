import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gold INTEGER NOT NULL,
                    civilians INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS builders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lumbermen (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS miners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS merchants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS military_units (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS buildings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    level INTEGER NOT NULL,
                    internal_upgrade_level INTEGER NOT NULL
                )
            ''')
            # Insert predefined building names
            cursor.execute('''
                INSERT INTO buildings (name, level, internal_upgrade_level)
                SELECT 'town hall', 0, 0 WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE name='town hall')
            ''')
            cursor.execute('''
                INSERT INTO buildings (name, level, internal_upgrade_level)
                SELECT 'lumbermill', 0, 0 WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE name='lumbermill')
            ''')
            cursor.execute('''
                INSERT INTO buildings (name, level, internal_upgrade_level)
                SELECT 'recruiting hall', 0, 0 WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE name='recruiting hall')
            ''')
            cursor.execute('''
                INSERT INTO buildings (name, level, internal_upgrade_level)
                SELECT 'mines', 0, 0 WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE name='mines')
            ''')
            cursor.execute('''
                INSERT INTO buildings (name, level, internal_upgrade_level)
                SELECT 'merchants guild', 0, 0 WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE name='merchants guild')
            ''')
            cursor.execute('''
                INSERT INTO buildings (name, level, internal_upgrade_level)
                SELECT 'army base', 0, 0 WHERE NOT EXISTS (SELECT 1 FROM buildings WHERE name='army base')
            ''')
            conn.commit()

    def save_resource(self, gold, civilians):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO resources (gold, civilians)
                VALUES (?, ?)
            ''', (gold, civilians))
            conn.commit()

    def load_resources(self):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM resources')
            return cursor.fetchall()

# Example usage:
if __name__ == "__main__":
    db = Database('test.db')
    db.create_table()
    db.save_resource(100, 50)
    resources = db.load_resources()
    print(resources)