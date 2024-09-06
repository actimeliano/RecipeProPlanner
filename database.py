import sqlite3
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Recipe:
    id: Optional[int]
    name: str
    category: str
    ingredients: List[str]
    instructions: str

class RecipeDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('recipes.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_recipe(self, recipe: Recipe):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO recipes (name, category, ingredients, instructions)
        VALUES (?, ?, ?, ?)
        ''', (recipe.name, recipe.category, ','.join(recipe.ingredients), recipe.instructions))
        self.conn.commit()

    def get_all_recipes(self) -> List[Recipe]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM recipes')
        return [Recipe(id=row[0], name=row[1], category=row[2], ingredients=row[3].split(','), instructions=row[4])
                for row in cursor.fetchall()]

    def search_recipes(self, search_term: str, category: str) -> List[Recipe]:
        cursor = self.conn.cursor()
        query = 'SELECT * FROM recipes WHERE name LIKE ?'
        params = [f'%{search_term}%']
        
        if category != "All":
            query += ' AND category = ?'
            params.append(category)
        
        cursor.execute(query, params)
        return [Recipe(id=row[0], name=row[1], category=row[2], ingredients=row[3].split(','), instructions=row[4])
                for row in cursor.fetchall()]

    def __del__(self):
        self.conn.close()
