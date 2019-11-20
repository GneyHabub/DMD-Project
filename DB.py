import psycopg2
from psycopg2 import Error


class DB:
    def __init__(self,user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432", database = "postgres"):
        self.connection = psycopg2.connect( user = user,
                                            password = password,
                                            host = host,
                                            port = port,
                                            database = database)
        print("PostgreSQL connection is Opened")
        self.cursor = self.connection.cursor()
        print("Creating the DB")
        self.pg_query("schema.sql")
        print("Finish creating the DB")
    
    def pg_query(self, query):
        try:
            if(".sql" in str(query)):
                self.cursor.execute(open(query, "r").read())
                print("{:} has been created".format(query))

            else:
                self.cursor.execute(query)
                print("Query that start with \n\"{:}\"\n has been executed and added to the database".format(query[:min(len(query),10)]))


            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error :
            print (error)


    def __del__(self):
        if(self.connection):
            self.cursor.close()
            self.connection.close
        print("PostgreSQL connection is closed")

if __name__ == "__main__":
    db = DB()
