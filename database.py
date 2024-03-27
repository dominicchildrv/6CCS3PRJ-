# database.py

import sqlite3

class PacmanDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()
        self.setup_table()

    def create_connection(self):
        """Create a database connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except sqlite3.Error as e:
            print(e)
        return None

    def setup_table(self):
        """Create a table for storing Pacman layouts."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS layouts (
            id integer PRIMARY KEY,
            layout_name text NOT NULL,
            layout_ghosts int NOT NULL
        ); """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    def insert_layout(self, layout_name, layout_ghosts):
        """Insert a new layout into the layouts table."""
        sql = '''INSERT INTO layouts(layout_name, layout_ghosts)
                 VALUES(?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, (layout_name, layout_ghosts))
        self.conn.commit()
        return cur.lastrowid
    
    def get_layout(self, layout_name):
        """ Query layout by layout_name """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM layouts WHERE layout_name=?", (layout_name,))

        row = cur.fetchone()

        if row:
            return row
        else:
            return None

    def layout_name_exists(self, layout_name):
        """Check if a layout name already exists in the database."""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM layouts WHERE layout_name=?", (layout_name,))
        count = cur.fetchone()[0]
        return count > 0
    
    def get_all_layouts(self):
        """Fetch all layouts from the database."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM layouts")
        return cur.fetchall()
    
    def delete_layout_by_id(self, id):
        """Delete a layout by its ID."""
        sql = 'DELETE FROM layouts WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()
        return cur.rowcount  # Returns the number of rows deleted
