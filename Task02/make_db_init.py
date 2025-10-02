import csv
import os

def generate_sql_script():
    sql_content = []
    
    # Начало SQL-файла
    sql_content.append("-- SQLite script for creating movies_rating database")
    sql_content.append("-- Generated automatically")
    sql_content.append("")
    
    # Удаление существующих таблиц
    sql_content.append("-- Drop existing tables")
    sql_content.append("DROP TABLE IF EXISTS movies;")
    sql_content.append("DROP TABLE IF EXISTS ratings;")
    sql_content.append("DROP TABLE IF EXISTS tags;")
    sql_content.append("DROP TABLE IF EXISTS users;")
    sql_content.append("")
    
    # Создание таблиц
    sql_content.append("-- Create tables")
    
    # Таблица movies
    sql_content.append("CREATE TABLE movies (")
    sql_content.append("    id INTEGER PRIMARY KEY,")
    sql_content.append("    title TEXT NOT NULL,")
    sql_content.append("    year INTEGER,")
    sql_content.append("    genres TEXT")
    sql_content.append(");")
    sql_content.append("")
    
    # Таблица ratings
    sql_content.append("CREATE TABLE ratings (")
    sql_content.append("    id INTEGER PRIMARY KEY,")
    sql_content.append("    user_id INTEGER NOT NULL,")
    sql_content.append("    movie_id INTEGER NOT NULL,")
    sql_content.append("    rating REAL NOT NULL,")
    sql_content.append("    timestamp INTEGER NOT NULL")
    sql_content.append(");")
    sql_content.append("")
    
    # Таблица tags
    sql_content.append("CREATE TABLE tags (")
    sql_content.append("    id INTEGER PRIMARY KEY,")
    sql_content.append("    user_id INTEGER NOT NULL,")
    sql_content.append("    movie_id INTEGER NOT NULL,")
    sql_content.append("    tag TEXT NOT NULL,")
    sql_content.append("    timestamp INTEGER NOT NULL")
    sql_content.append(");")
    sql_content.append("")
    
    # Таблица users
    sql_content.append("CREATE TABLE users (")
    sql_content.append("    id INTEGER PRIMARY KEY,")
    sql_content.append("    name TEXT NOT NULL,")
    sql_content.append("    email TEXT NOT NULL,")
    sql_content.append("    gender TEXT NOT NULL,")
    sql_content.append("    register_date TEXT NOT NULL,")
    sql_content.append("    occupation TEXT NOT NULL")
    sql_content.append(");")
    sql_content.append("")
    
    # Загрузка данных в таблицу movies
    sql_content.append("-- Load data into movies table")
    with open('dataset/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Извлекаем год из названия (формат: "Название (год)")
            title = row['title'].replace("'", "''")
            year = None
            if '(' in title and ')' in title:
                try:
                    year = int(title[-5:-1])
                except:
                    year = None
            
            genres = row['genres'].replace("'", "''")
            
            sql_content.append(f"INSERT INTO movies (id, title, year, genres) VALUES ({row['movieId']}, '{title}', {year if year else 'NULL'}, '{genres}');")
    sql_content.append("")
    
    # Загрузка данных в таблицу ratings
    sql_content.append("-- Load data into ratings table")
    with open('dataset/ratings.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            sql_content.append(f"INSERT INTO ratings (id, user_id, movie_id, rating, timestamp) VALUES ({i}, {row['userId']}, {row['movieId']}, {row['rating']}, {row['timestamp']});")
    sql_content.append("")
    
    # Загрузка данных в таблицу tags
    sql_content.append("-- Load data into tags table")
    with open('dataset/tags.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            tag = row['tag'].replace("'", "''")
            sql_content.append(f"INSERT INTO tags (id, user_id, movie_id, tag, timestamp) VALUES ({i}, {row['userId']}, {row['movieId']}, '{tag}', {row['timestamp']});")
    sql_content.append("")
    
    # Загрузка данных в таблицу users
    sql_content.append("-- Load data into users table")
    with open('dataset/users.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                user_id, name, email, gender, register_date, occupation = parts
                name = name.replace("'", "''")
                email = email.replace("'", "''")
                occupation = occupation.replace("'", "''")
                
                sql_content.append(f"INSERT INTO users (id, name, email, gender, register_date, occupation) VALUES ({user_id}, '{name}', '{email}', '{gender}', '{register_date}', '{occupation}');")
    sql_content.append("")
    
    # Запись в файл
    with open('db_init.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_content))
    
    print("SQL script generated: db_init.sql")
    print("To create database run: sqlite3 movies_rating.db < db_init.sql")

if __name__ == "__main__":
    generate_sql_script()