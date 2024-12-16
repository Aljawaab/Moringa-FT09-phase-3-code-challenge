from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, title, content, author_id, magazine_id):
        # Validate inputs
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters.")
        if not isinstance(content, str):
            raise ValueError("Content must be a string.")
        if not isinstance(author_id, int) or not isinstance(magazine_id, int):
            raise ValueError("author_id and magazine_id must be integers.")
        
        # Insert the article into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (title, content, author_id, magazine_id),
        )
        conn.commit()
        conn.close()

        
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author(self):
        """Return the Author instance for this article."""
        return Author(self._author_id, "Unknown")

    @property
    def magazine(self):
        """Return the Magazine instance for this article."""
        return Magazine(self._magazine_id, "Unknown", "Unknown")

    def __repr__(self):
        return f"<Article {self.title}>"
