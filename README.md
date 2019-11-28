# DMD-Project
Software project in DMD course at Innopolis University by Hany Hamed, Alexandr Grischenko and Alexandr Krivonosov (2019)


** How to use the Database?

1- Install postgres from that [link](https://www.2ndquadrant.com/en/blog/pginstaller-install-postgresql/) and setup the environment or it depends on your machine, it is easier on linux OS.

1.1- and install faker library from [here](https://github.com/joke2k/faker) and psycopg2 from [here](http://initd.org/psycopg/).

1.2- Good links for configuration and running postgres:
    
* [Link1](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html)

* [Link2](https://tecadmin.net/install-postgresql-server-on-ubuntu/)



2- Modify the password to "123456789" and the user "user".

3- You need to create a Database with the name "Hospital" in postgres using: ```sudo -u postgres createdb Hospital```.


4- Run ```sudo -u postgres psql -d Hospital ``` to run the database shell.

5- Type \c to connect to the database.

6- Run ```generate.py``` using ```python3 generate.py``` to generate fake data for testing.

7- Run ```main.py``` using ```python3 main.py``` to run the main program that is responsible for the queries.

8- To restore the schemas original files run ```./restore_schemas.sh```
