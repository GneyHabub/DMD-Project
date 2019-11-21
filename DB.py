import psycopg2
from psycopg2 import Error
from faker import Faker
import json
import csv
import numpy as np
 


class DB:
    def __init__(self,user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432", database = "postgres"):
        self.fake = Faker()
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
        # self.load_db()
        # self.pg_query('INSERT INTO person VALUES (996,"Ryan Garcia","odavis@gmail.com","mitchelljulie","CWsbkbjPfTRm","M",1932-12-31,87,2)')
    
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


    def load_db(self, db_name=None):
        if(type(db_name) is str):
            with open("data/"+db_name, 'r') as file:
                next(file)
                # print(file.read())
                self.cursor.copy_from(file, db_name[:-4], sep=',')
                self.connection.commit()

        elif(db_name is None):
            # make the normal one (the default)
            pass
        elif(type(db_name) is list):
            for i in db_name:
                with open("data/"+i, 'r') as file:
                    next(file)
                    # print(file.read())
                    self.cursor.copy_from(file, i[:-4], sep=',')
                    self.connection.commit()
            
    def generate(self, table_name=None, write_schema_flag=False, write_json_flag=True):
        if(table_name == "person"):
            self._generate_person(write_json_flag=write_json_flag, write_schema_flag=write_schema_flag)
        else:
            pass
    
    def _generate_person(self, num=5, write_schema_flag=False, write_json_flag=True):
        person = []
        contact_details = []
        for i in range(0, num):
            person.append({})
            contact_details.append({})
            
            profile = self.fake.profile()
            person[i]["id"]= self.fake.random_int(1, 1000)+i+1
            person[i]["full_name"]= profile["name"]
            person[i]["email"] = profile["mail"]
            person[i]["user_login"] = profile["username"]
            person[i]["user_password"] = "".join(self.fake.random_letters(length=self.fake.random_int(7, 15)))
            person[i]["sex"] = profile["sex"]
            person[i]["date_of_birth"] = profile["birthdate"]
            person[i]["age"] = 2019 - person[i]["date_of_birth"].year
            person[i]["permission_level"] = self.fake.random_int(1, 5)

            contact_details[i]["id"] = person[i]["id"]
            contact_details[i]["phone"] = self.fake.phone_number()[:20]
            contact_details[i]["telegram"] = "@"+profile["username"]
            contact_details[i]["other"] = "".join(self.fake.random_letters(length=30) if i%5 else "")
            
            #reseptionist, maintanence_worker, cleaning_team_worker, security_team_member, hr, pharmasist,
            # cook, priest, nurse, IT_specialist, prof, doctor, patient, lab_technician
            person_type_selector = np.random.choice(13,1,p=[0.2,0.15,0.2,0.1,0.05,0.05,0.05,0.05,0.04,0.03,0.03,0.03,0.02])
            if(i == 0):
                pass    # head doctor
            elif(i == 1):
                pass    # head nurse
            elif(person_type_selector == 0):
                pass # nurse
            elif(person_type_selector == 1):
                pass # doctor
            elif(person_type_selector == 2):
                pass # patient
            elif(person_type_selector == 3):
                pass # prof
            elif(person_type_selector == 4):
                pass # lab_technician
            elif(person_type_selector == 5):
                pass #cleaning_team_worker
            elif(person_type_selector == 6):
                pass #reseptionist
            elif(person_type_selector == 7):
                pass #maintanence_worker
            elif(person_type_selector == 8):
                pass #security_team_member
            elif(person_type_selector == 9):
                pass #hr
            elif(person_type_selector == 10):
                pass #pharmasist
            elif(person_type_selector == 11):
                pass #cook
            elif(person_type_selector == 12):
                pass #IT_specialist
            elif(person_type_selector == 13):
                pass #priest
            if(write_schema_flag):
                with open('data/person.sql', 'a+') as append_file:
                    append_file.write("\nINSERT INTO person VALUES ({:}, '{:}', '{:}', '{:}', '{:}','{:}','{:}',{:},{:});".format(person[i]["id"],person[i]["full_name"],person[i]["email"],person[i]["user_login"],person[i]["user_password"],person[i]["sex"],person[i]["date_of_birth"],person[i]["age"],person[i]["permission_level"]))
            
            if(write_schema_flag):
                with open('data/contact_details.sql', 'a+') as append_file:
                    append_file.write("\nINSERT INTO contact_details VALUES ({:}, '{:}', '{:}', '{:}');".format(contact_details[i]["id"],contact_details[i]["phone"],contact_details[i]["telegram"],contact_details[i]["other"]))

        if(write_json_flag):
            with open('data/person.csv', 'w') as writeFile:
                writer = csv.DictWriter(writeFile, fieldnames=list(person[0].keys()))
                writer.writeheader()
                for data in person:
                    writer.writerow(data)

            with open('data/contact_details.csv', 'w') as writeFile:
                writer = csv.DictWriter(writeFile, fieldnames=list(contact_details[0].keys()))
                writer.writeheader()
                for data in contact_details:
                    writer.writerow(data)
        
        
if __name__ == "__main__":
    db = DB()
    db.generate("person",write_schema_flag=True)
    db.load_db(["person.csv","contact_details.csv"])
