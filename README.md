# LBTask

The project requires Python 3.x. Other requirements are in "requirements.txt".
psycopg2 module is needed only for starting the project with PostreSQL.

To start the server with SQLite (populated database already exists in repository):
- python manage.py runserver

But there are some problems with function UPPER() there so it's highly recommended to use PostreSQL.

To start project with PostgreSQL:

1) Change database parameters in LBTask/db.json
2) python manage.py migrate
3) python manage.py PopulateDB --number 100
4) python manage.py runserver

The number option on step 3 is the number of documents that will be randomly populated.

Enjoy :)
