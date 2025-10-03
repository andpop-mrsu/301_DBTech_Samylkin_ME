@echo off
python make_db_init.py
sqlite3 movies_rating.db < db_init.sql
echo Database movies_rating.db created successfully!
pause