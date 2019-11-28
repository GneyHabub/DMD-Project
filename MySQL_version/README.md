# MySQL part


**How to use the Database?

1- Install MySQL from that [link](https://www.sitepoint.com/how-to-install-mysql/) and setup the environment or it depends on your machine, it is easier on linux OS.


1.1- and install faker library from [here](https://github.com/joke2k/faker) and pymysql from [here](https://pypi.org/project/PyMySQL/).

1.2- Good links for configuration and running Mysql:
    
* [Link](https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/)

* [Link2](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql)

2- You need to create a "user" user and give it all the privileges from the root user and modify the password to "123456789". More details in link2.

4- Run ```sudo mysql  -u user -p Hospital``` to run the database shell.

5- Type ```connect Hospital``` to connect to the database.

6- Run ```generate.py``` using ```python3 generate.py``` to generate fake data for testing.


