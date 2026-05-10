"""
Database module for Smart Budget Planner
Handles SQLite database operations and initialization
"""

import sqlite3
import os
from datetime import datetime

# Database file path
DB_PATH = 'database.db'


def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_database():
    """
    Initialize the database with required tables
    Creates 'expenses' and 'budget' tables if they don't exist
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    
    # Create budget table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monthly_limit REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if budget table has default value, if not insert it
    cursor.execute('SELECT COUNT(*) FROM budget')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO budget (monthly_limit) VALUES (?)', (5000.0,))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def add_expense(amount, category, description, date):
    """
    Add a new expense to the database
    
    Args:
        amount (float): Expense amount
        category (str): Expense category
        description (str): Expense description
        date (str): Expense date (YYYY-MM-DD format)
    
    Returns:
        int: ID of the inserted expense
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, category, description, date))
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        return expense_id
    except Exception as e:
        print(f"Error adding expense: {e}")
        return None


def get_all_expenses():
    """
    Fetch all expenses from the database
    
    Returns:
        list: List of all expenses
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = cursor.fetchall()
        conn.close()
        return [dict(expense) for expense in expenses]
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        return []


def get_expense_by_id(expense_id):
    """
    Fetch a single expense by ID
    
    Args:
        expense_id (int): Expense ID
    
    Returns:
        dict: Expense data or None if not found
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        expense = cursor.fetchone()
        conn.close()
        return dict(expense) if expense else None
    except Exception as e:
        print(f"Error fetching expense: {e}")
        return None


def update_expense(expense_id, amount, category, description, date):
    """
    Update an existing expense
    
    Args:
        expense_id (int): Expense ID
        amount (float): Updated amount
        category (str): Updated category
        description (str): Updated description
        date (str): Updated date
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE expenses
            SET amount = ?, category = ?, description = ?, date = ?
            WHERE id = ?
        ''', (amount, category, description, date, expense_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating expense: {e}")
        return False


def delete_expense(expense_id):
    """
    Delete an expense from the database
    
    Args:
        expense_id (int): Expense ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting expense: {e}")
        return False


def set_monthly_budget(amount):
    """
    Set or update the monthly budget
    
    Args:
        amount (float): Monthly budget limit
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE budget SET monthly_limit = ? WHERE id = 1', (amount,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error setting budget: {e}")
        return False


def get_monthly_budget():
    """
    Get the current monthly budget
    
    Returns:
        float: Monthly budget limit
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT monthly_limit FROM budget WHERE id = 1')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 5000.0
    except Exception as e:
        print(f"Error fetching budget: {e}")
        return 5000.0


def get_total_expenses():
    """
    Calculate total expenses for the current month
    
    Returns:
        float: Sum of all expenses in current month
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        current_date = datetime.now()
        year_month = f"{current_date.year}-{current_date.month:02d}"
        
        cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE date LIKE ?
        ''', (f"{year_month}%",))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] else 0.0
    except Exception as e:
        print(f"Error calculating total expenses: {e}")
        return 0.0


def get_expenses_by_category():
    """
    Get total expenses grouped by category
    
    Returns:
        dict: Dictionary with categories as keys and amounts as values
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        current_date = datetime.now()
        year_month = f"{current_date.year}-{current_date.month:02d}"
        
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE date LIKE ?
            GROUP BY category
            ORDER BY total DESC
        ''', (f"{year_month}%",))
        
        results = cursor.fetchall()
        conn.close()
        return {row['category']: row['total'] for row in results}
    except Exception as e:
        print(f"Error fetching expenses by category: {e}")
        return {}


if __name__ == '__main__':
    init_database()
