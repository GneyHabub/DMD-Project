# sudo -u postgres psql <DB_name>
# To run postgres: sudo -u postgres psql postgress
def test_create_db():
    import psycopg2
    from psycopg2 import Error

    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "123456789",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "postgres")
        cursor = connection.cursor()
        
        create_table_query = '''CREATE TABLE mobile
            (ID INT PRIMARY KEY     NOT NULL,
            MODEL           TEXT    NOT NULL,
            PRICE         REAL); '''
        
        cursor.execute(create_table_query)
        connection.commit()
        print("DB created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
        print (error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def test_faking_data():
    #http://zetcode.com/python/faker/
    #https://www.geeksforgeeks.org/python-faker-library/
    from faker import Faker
    import json
    import csv
    from DB import DB
    fake = Faker()
    person = [] 
    for i in range(0, 5): 
        person.append({})
        profile = fake.profile()
        person[i]["id"]= fake.random_int(1, 1000) 
        person[i]["full_name"]= profile["name"]
        person[i]["email"] = profile["mail"]
        person[i]["user_login"] = profile["username"]
        person[i]["user_password"] = "".join(fake.random_letters(length=fake.random_int(7, 15)))
        person[i]["sex"] = profile["sex"]
        person[i]["date_of_birth"] = profile["birthdate"]
        person[i]["age"] = 2019 - person[i]["date_of_birth"].year
        person[i]["permission_level"] = fake.random_int(1, 5)
    print(person) 
    with open('person.csv', 'w') as writeFile:
        writer = csv.DictWriter(writeFile, fieldnames=list(person[0].keys()))
        writer.writeheader()
        for data in person:
            writer.writerow(data)

    db = DB()
    db.
  
    # dictionary dumped as json in a json file 
    # with open('data.json', 'w') as fp: 
    #     json.dump(data, fp) 

if __name__ == "__main__":
    test_faking_data()