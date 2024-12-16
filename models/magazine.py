from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        # Validate inputs
        if not isinstance(id, int):
            raise ValueError("ID must be an integer.")
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters.")
        if not isinstance(category, str) or len(category.strip()) == 0:
            raise ValueError("Category must be a non-empty string.")
        
        # Insert or fetch magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM magazines WHERE id = ?", (id,))
        existing_magazine = cursor.fetchone()

        if not existing_magazine:
            cursor.execute(
                "INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)",
                (id, name, category),
            )
            conn.commit()
        conn.close()

        self._id = id
        self._name = name
        self._category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str) or not (2 <= len(new_name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters.")
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if not isinstance(new_category, str) or len(new_category.strip()) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = new_category

    def articles(self):
        """Fetch all articles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        """Fetch all authors who have written articles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT DISTINCT a.*
            FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """
        cursor.execute(sql, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors

    def article_titles(self):
        """Fetch a list of article titles for this magazine."""
        articles = self.articles()
        return [article["title"] for article in articles] if articles else None

    def contributing_authors(self):
        """Fetch authors with more than 2 articles in this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT a.*, COUNT(*) as article_count
            FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """
        cursor.execute(sql, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors if authors else None

    def __repr__(self):
        return f"<Magazine {self.name}, Category: {self.category}>"
