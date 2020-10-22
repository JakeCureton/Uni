# Uni
A fun little cash machine experiment. Started off in terminal and then attached an rpi4 to a matrix keypad and shazam, the code continues to grow.

RUN:

LOCAL
use ATM.py in pycharm or terminal. No dependancies needed.
default pin is 1234 or bypass! for more money.

MySQL 
use atm-mysql.py in pycharm and ensure to install package needed.
Preferences > Project > + > search mysql-connector-python

You also need a local MySQL server "https://dev.mysql.com/downloads/mysql/". 

Once installed, use a database tool such as HeidiSql to connect and create a database. 

Download customers.sql from this git and import into your database using HeidiSql.

Change the variables line 11 onwards to match your database connection.

Default pin is 1234
