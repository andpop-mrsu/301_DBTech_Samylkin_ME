#!/bin/bash
chcp 65001

sqlite3 movies_rating.db < db_init.sql

echo "1. Найти все пары пользователей, оценивших один и тот же фильм. Устранить дубликаты, проверить отсутствие пар с самим собой."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT DISTINCT u1.name as user1, u2.name as user2, m.title FROM ratings r1 JOIN ratings r2 ON r1.movie_id = r2.movie_id AND r1.user_id < r2.user_id JOIN users u1 ON r1.user_id = u1.id JOIN users u2 ON r2.user_id = u2.id JOIN movies m ON r1.movie_id = m.id ORDER BY u1.name, u2.name LIMIT 100;"
echo " "

echo "2. Найти 10 самых свежих оценок от разных пользователей, вывести названия фильмов, имена пользователей, оценку, дату отзыва."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT m.title, u.name, r.rating, datetime(r.timestamp, 'unixepoch') as rating_date FROM ratings r JOIN users u ON r.user_id = u.id JOIN movies m ON r.movie_id = m.id ORDER BY r.timestamp DESC LIMIT 10;"
echo " "

echo "3. Вывести в одном списке все фильмы с максимальным средним рейтингом и все фильмы с минимальным средним рейтингом."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "WITH avg_ratings AS ( SELECT m.id, m.title, m.year, AVG(r.rating) as avg_rating FROM movies m JOIN ratings r ON m.id = r.movie_id GROUP BY m.id, m.title, m.year ), min_max AS ( SELECT MIN(avg_rating) as min_rating, MAX(avg_rating) as max_rating FROM avg_ratings ) SELECT ar.title, ar.year, ar.avg_rating, CASE WHEN ar.avg_rating = (SELECT max_rating FROM min_max) THEN 'Да' ELSE 'Нет' END as Рекомендуем FROM avg_ratings ar WHERE ar.avg_rating = (SELECT min_rating FROM min_max) OR ar.avg_rating = (SELECT max_rating FROM min_max) ORDER BY ar.year, ar.title;"
echo " "

echo "4. Вычислить количество оценок и среднюю оценку, которую дали фильмам пользователи-женщины в период с 2010 по 2012 год."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT COUNT(*) as ratings_count, AVG(r.rating) as avg_rating FROM ratings r JOIN users u ON r.user_id = u.id WHERE u.gender = 'female' AND strftime('%Y', datetime(r.timestamp, 'unixepoch')) BETWEEN '2010' AND '2012';"
echo " "

echo "5. Составить список фильмов с указанием их средней оценки и места в рейтинге по средней оценке."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT m.year, m.title, AVG(r.rating) as avg_rating, RANK() OVER (ORDER BY AVG(r.rating) DESC) as rating_rank FROM movies m JOIN ratings r ON m.id = r.movie_id GROUP BY m.id, m.title, m.year ORDER BY m.year, m.title LIMIT 20;"
echo " "

echo "6. Вывести список из 10 последних зарегистрированных пользователей в формате 'Фамилия Имя|Дата регистрации'."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT name, register_date FROM users ORDER BY register_date DESC LIMIT 10;"
echo " "

echo "7. С помощью рекурсивного CTE составить таблицу умножения для чисел от 1 до 10."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "WITH RECURSIVE numbers(n) AS ( SELECT 1 UNION ALL SELECT n+1 FROM numbers WHERE n < 10 ), multiplication_table AS ( SELECT a.n as a, b.n as b, a.n * b.n as result FROM numbers a, numbers b ) SELECT a || 'x' || b || '=' || result FROM multiplication_table ORDER BY a, b;"
echo " "

echo "8. С помощью рекурсивного CTE выделить все жанры фильмов, имеющиеся в таблице movies."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "WITH RECURSIVE split_genres(movie_id, genre, remaining) AS ( SELECT id, substr(genres, 1, instr(genres || '|', '|') - 1), substr(genres || '|', instr(genres || '|', '|') + 1) FROM movies WHERE genres != '' UNION ALL SELECT movie_id, substr(remaining, 1, instr(remaining || '|', '|') - 1), substr(remaining || '|', instr(remaining || '|', '|') + 1) FROM split_genres WHERE remaining != '' ) SELECT DISTINCT genre FROM split_genres ORDER BY genre;"
echo " "

pause