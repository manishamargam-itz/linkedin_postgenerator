import sqlite3
import json
from datetime import datetime

class DatabaseHelper:
    def __init__(self, db_name="linkedin_posts.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                topic TEXT NOT NULL,
                length TEXT NOT NULL,
                language TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_template BOOLEAN DEFAULT 0,
                engagement_score INTEGER DEFAULT 0
            )
        ''')

        # Create templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create user_preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                use_emojis BOOLEAN DEFAULT 1,
                show_hashtags BOOLEAN DEFAULT 1,
                default_length TEXT DEFAULT 'Medium',
                default_language TEXT DEFAULT 'English',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_post(self, content, topic, length, language, is_template=False):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO posts (content, topic, length, language, is_template)
            VALUES (?, ?, ?, ?, ?)
        ''', (content, topic, length, language, is_template))
        conn.commit()
        conn.close()

    def get_all_posts(self, limit=10, offset=0):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM posts 
            WHERE is_template = 0
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        posts = cursor.fetchall()
        conn.close()
        return posts

    def get_templates(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM templates')
        templates = cursor.fetchall()
        conn.close()
        return templates

    def save_template(self, name, content, category):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO templates (name, content, category)
            VALUES (?, ?, ?)
        ''', (name, content, category))
        conn.commit()
        conn.close()

    def save_user_preferences(self, use_emojis, show_hashtags, default_length, default_language):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_preferences (use_emojis, show_hashtags, default_length, default_language)
            VALUES (?, ?, ?, ?)
        ''', (use_emojis, show_hashtags, default_length, default_language))
        conn.commit()
        conn.close()

    def get_user_preferences(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_preferences ORDER BY created_at DESC LIMIT 1')
        preferences = cursor.fetchone()
        conn.close()
        return preferences

    def delete_post(self, post_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()

    def update_post_engagement(self, post_id, engagement_score):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE posts 
            SET engagement_score = ?
            WHERE id = ?
        ''', (engagement_score, post_id))
        conn.commit()
        conn.close() 