from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        # Validate inputs
        if not isinstance(id, int):
            raise ValueError("ID must be an integer.")
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Name must be a non-empty string.")
        
        # Check if the author already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM authors WHERE id = ?", (id,))
        existing_author = cursor.fetchone()

        if not existing_author:
            # Insert new author into the database
            cursor.execute("INSERT INTO authors (id, name) VALUES (?, ?)", (id, name))
            conn.commit()
        conn.close()
        
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        """Fetch all articles written by this author."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM articles WHERE author_id = ?"
        cursor.execute(sql, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        """Fetch all magazines this author has contributed to."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT DISTINCT m.* 
            FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """
        cursor.execute(sql, (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines

    def __repr__(self):
        return f"<Author {self.name}>"
