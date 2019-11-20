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
    fake = Faker()
    print(fake.name())
    print(fake.random_int(min=0, max=5, step=1))
    
    print(fake.email())
    print(fake.profile())

    # data ={} 
    # for i in range(0, x): 
    #     data[i]={} 
    #     data[i]['id']= fake.random_int(1, 100) 
    #     data[i]['name']= fake.name() 
    #     data[i]['address']= fake.address() 
    #     data[i]['latitude']= str(fake.latitude()) 
    #     data[i]['longitude']= str(fake.longitude()) 
    # print(data) 
  
    # dictionary dumped as json in a json file 
    # with open('data.json', 'w') as fp: 
    #     json.dump(data, fp) 

if __name__ == "__main__":
    test_faking_data()