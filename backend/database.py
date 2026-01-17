import sqlite3
import os

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    
    # it needs convert rows to list of dicts because sqlite3.row is not JSON serializable
    #users_list = []
    #for user in users:
        #users_list.append({
    #        'id': user['id'],
    #        'name': user['name'],
    #        'email': user['email'],
    #        'age': user['age']
    #    })
        
    return [dict(user) for user in users]

def create_user(name, email, age):
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
        (name, email, age)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": user_id,
        "name": name,
        "email": email,
        "age": age
    }

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user:
        return {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'age': user['age']
        }
    return None

def update_user(user_id, name, email, age):
    conn = get_db_connection()
    
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return None

    conn.execute(
        'UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?',
        (name, email, age, user_id)
    )
    conn.commit()
    conn.close()
    
    return {
        'id': user_id,
        'name': name,
        'email': email,
        'age': age
    }

def delete_user(user_id):
    conn = get_db_connection()
    
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return None
    
    user_dict = {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'age': user['age']
    }
    
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return user_dict

def get_users_count():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    conn.close()
    return count

def clear_all_users():
    conn = get_db_connection()
    conn.execute('DELETE FROM users')
    conn.commit()
    conn.close()
    print("All users deleted!")

init_db()