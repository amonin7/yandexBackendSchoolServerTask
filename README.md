# yandexBackendSchoolServerTask

## Задание
Интернет-магазин подарков хочет запустить акцию в разных регионах. Чтобы стратегия продаж была эффективной, необходимо произвести анализ рынка.
У магазина есть поставщик, регулярно присылающий выгрузки данных с информацией о жителях. Проанализировав их, можно выявить спрос на подарки в разных городах
у жителей разных возрастных групп по месяцам.
Ваша задача - разработать на python REST API сервис, который сохраняет переданные ему наборы данных (выгрузки от поставщика) c жителями, позволяет их просматривать, редактировать информацию об отдельных жителях, а также производить анализ возрастов жителей по городам и анализировать спрос на подарки в разных месяцах для указанного набора данных.
Должна быть реализована возможность загрузить несколько независимых наборов данных с разными идентификаторами, независимо друг от друга изменять
и анализировать их.
Сервис необходимо развернуть на предоставленной виртуальной машине на 0.0.0.0:8080.

### Шаги по запуску и установке приложения:
1. Install PostgreSQL in Linux using the command,
sudo apt-get install postgresql postgresql-contrib
2. Now create a superuser for PostgreSQL
sudo -u postgres createuser --superuser name_of_user
3. And create a database using created user account
sudo -u name_of_user createdb citizensdb
4. Now you can check the created database with,
psql -U name_of_user -d citizensdb
5. To create virtual environments we need virtualenv package. Install python virtualenv package using,
pip install virtualenv
6. Create a virtual environment named env inside the created directory by,
virtualenv env
7. To activate this environment use this command inside books_server directory.
source env/bin/activate
You should log into books_store data base if above command was success.
8. Install a requirements, by
pip install reqirements.txt
9. According to created configurations set “APP_SETTINGS” environment variable by running this in the terminal
export APP_SETTINGS="config.DevelopmentConfig"
10. export DATABASE_URL="postgresql:///citizensdb"
11. Migrating database. First run,
python manage.py db init
12. To migrate using these created files, run
python manage.py db migrate
13. Now apply the migrations to the database using
python manage.py db upgrade
(ADDITIONAL: In a case of migration fails to be success try droping auto generated alembic_version table by 
drop table alembic_version;
14. we can run our server by,
python manage.py runserver
