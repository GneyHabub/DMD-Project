import psycopg2
from psycopg2 import Error
from faker import Faker
import json
import csv
import numpy as np
 


class DB:
    def __init__(self,user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432", database = "postgres"):
        # Source: https://www.webmd.com/health-insurance/insurance-doctor-types#1
        self.speciality_list = ["Allergist", "Anesthesiologist", "Cardiologist", "Colon Surgeon"
                               ,"Critical Care Medicine Specialist", "Dermatologist", "Endocrinologists"
                               ,"Emergency Medicine Specialist", "Emergency Medicine Specialist"
                               ,"Gastroenterologist", "Geriatric Medicine Specialist", "Hematologist"
                               ,"Infectious Disease Specialist", "Hospice and Palliative Medicine Specialist"
                               ,"Internist", "Medical Geneticist", "Nephrologist", "Neurologist"
                               ,"Obstetrician and Gynecologist", "Oncologist", "Ophthalmologist"
                               ,"Osteopath", "Otolaryngologist", "Pathologist", "Pediatrician"
                               ,"Physiatrist", "Plastic Surgeon", "Podiatrist", "Preventive Medicine Specialist"
                               ,"Psychiatrist", "Pulmonologist", "Radiologist", "Rheumatologist"
                               ,"Medicine Specialist", "Sports Medicine Specialist", "General Surgeon", "Urologist"]
        
        # Source: https://www.disabled-world.com/definitions/hospital-departments.php
        self.departement_list = ["Breast Screening", "Cardiology", "Chaplaincy", "Critical Care", "Discharge Lounge", "Gynecology"
                                ,"Health & Safety", "Microbiology", "Maternity", "Infection Control", "Intensive Care Unit"
                                ,"Haematology", "General Surgery", "Gastroenterology", "Diagnostic Imaging", "Neonatal"
                                ,"Neurology", "Nutrition", "Occupational Therapy", "Oncology", "Ophthalmology"
                                ,"Pain Management", "Radiology", "Urology"]
        self.valid_departement_list = []

        self.lab_list = []
        self.fake = Faker()
        self.connection = psycopg2.connect( user = user,
                                            password = password,
                                            host = host,
                                            port = port,
                                            database = database)
        self.num_departements = self.fake.random_int(10,20)

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
                print("{:} has been executed".format(query))

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
            
    def generate(self, num=5, table_name=None, write_schema_flag=True, write_json_flag=False):
        if(table_name == "person_member"):
            self._generate_person_member_db(num=num, write_json_flag=write_json_flag, write_schema_flag=write_schema_flag)
        else:
            # generate everything
            self._generate_facilities(write_json_flag=write_json_flag, write_schema_flag=write_schema_flag)
            self._generate_person_member_db(write_json_flag=write_json_flag, write_schema_flag=write_schema_flag)
    def clean_schema_files(self):
        f = open('data/dep_lab.sql', 'w')
        f.close()
        f = open('data/person_member.sql', 'w')
        f.close()

    def _generate_facilities(self, write_schema_flag=True, write_json_flag=False):
        self.valid_departement_list = self.fake.random_elements(elements=self.departement_list,length=self.num_departements,unique=True)
        num_labs_dep = self.fake.random_int(1,3)        
        for i in range(self.num_departements):
            departement = {"table_name": "departement", "id":i+1, "name": self.valid_departement_list[i]}
            labs = []
            for x in range(num_labs_dep):
                labs.append({"table_name": "lab", "id": x+i+2, "name": self.valid_departement_list[i]+" lab"+str(x+1), "departement_id": i+1})
                self.lab_list.append(self.valid_departement_list[i]+" lab"+str(x+1))
            
            with open('data/dep_lab.sql', 'a+') as append_file:
                self._generate_sql_schema(departement,append_file)
                for lab in labs:
                    self._generate_sql_schema(lab, append_file)

    def _generate_sql_schema(self, object, append_file):
        generation_string_header = "\nINSERT INTO {:} ({:}".format(object["table_name"],"id")
        generation_string_values = "VALUES ({:}".format(object["id"])
        for i in object.keys():
            if(i == "table_name" or i == "id"):
                continue
            generation_string_header += ",{:}".format(i)
            if(type(object[i]) == str):
                generation_string_values += ",'{:}'".format(object[i])
            elif(type(object[i]) == bool):
                generation_string_values += ",B'{:}'".format(int(object[i]))

            else:
                generation_string_values += ",{:}".format(object[i])
            
        generation_string = generation_string_header + ") " + generation_string_values + ");"
        
        append_file.write(generation_string)

    def _generate_person_member_db(self, num=5, write_schema_flag=True, write_json_flag=False):
        # using the property of aliasing and multi level functions
        def _staff_member_customizer(staff_member, position, salary, room):
            staff_member["position"] = position
            staff_member["salary"] = salary
            staff_member["room"] = room

        # person = []
        # contact_details = []
        # staff_member = []
        doctor_id_list = []
        for i in range(0, num):
            # person.append({})
            # contact_details.append({})
            person = {"table_name":"person"}
            contact_details = {}
            staff_member = {"table_name": "staff_member"}
            generated_member = {}
            patient = {"table_name":"patient"}
            

            profile = self.fake.profile()
            person["id"]= self.fake.random_int(1, 1000)+i+1
            person["first_name"]= profile["name"].split(" ")[0]
            person["second_name"]= profile["name"].split(" ")[1]
            person["email"] = profile["mail"]
            person["user_login"] = profile["username"]
            person["user_password"] = "".join(self.fake.random_letters(length=self.fake.random_int(7, 15)))
            person["sex"] = profile["sex"]
            person["date_of_birth"] = str(profile["birthdate"])
            person["age"] = 2019 - profile["birthdate"].year
            person["permission_level"] = self.fake.random_int(1, 5)

            contact_details["id"] = person["id"]
            contact_details["phone"] = self.fake.phone_number()[:20]
            contact_details["telegram"] = "@"+profile["username"]
            contact_details["other"] = "".join(self.fake.random_letters(length=30) if i%5 else "")
            
            # IT_complaint


            #reseptionist, maintanence_worker, cleaning_team_worker, security_team_member, hr, pharmasist,
            # cook, priest, nurse, IT_specialist, prof, doctor, patient, lab_technician
            person_type_selector = np.random.choice(13,1,p=[0.2,0.15,0.2,0.1,0.05,0.05,0.05,0.05,0.04,0.03,0.03,0.03,0.02])
            if(person_type_selector == 2):
                patient["id"] = person["id"]
                staff_member["registration_date"] = str(self.fake.date_between(start_date="-10d", end_date="today")) 
                staff_member["occupation"] = profile["job"][:50]

            else:
                # staff_member
                staff_member["id"] = person["id"]
                staff_member["employed_since"] = str(self.fake.date_between(start_date="-10y", end_date="today"))
                
                # Head Doctor
                if(i == 0):
                    _staff_member_customizer(staff_member, "Head Doctor", 100000, 1)
                    generated_member["table_name"] = "head_doctor"
                    generated_member["id"] = staff_member["id"]
                    generated_member["primary_speciality"] = self.fake.random_element(elements=self.speciality_list)
                
                # Head Nurse
                elif(i == 1):
                    _staff_member_customizer(staff_member, "Head Nurse", 80000, 2)
                    generated_member["table_name"] = "head_nurse"
                    generated_member["id"] = staff_member["id"]
                    generated_member["surgery_assistant"] = True
                
                # Nurse
                elif(person_type_selector == 0):
                    _staff_member_customizer(staff_member, "Nurse", 25000, self.fake.random_int(3,10))
                    generated_member["table_name"] = "nurse"
                    generated_member["id"] = staff_member["id"]
                    generated_member["surgery_assistant"] = bool(self.fake.random_int(0,1))
                    generated_member["preferred_shifts"] = self.fake.random_element(elements=["Night", "Day"])
                    generated_member["appointment_assistant"] = bool(self.fake.random_int(0,1))
                    generated_member["departement_id"] = self.fake.random_int(1,self.num_departements)

                # Doctor
                elif(person_type_selector == 1):
                    _staff_member_customizer(staff_member, "Doctor", 35000, self.fake.random_int(11,30))
                    generated_member["table_name"] = "doctor"
                    generated_member["id"] = staff_member["id"]
                    generated_member["speciality"] = self.fake.random_element(elements=self.speciality_list)
                    generated_member["emergency_hours"] = bool(self.fake.random_int(0,1))
                    generated_member["experience"] = self.fake.random_int(1,10) # At least have one year of experience after the graduation as a rule for graduation to work for one year and then they can take their certificate
                    generated_member["departement_id"] = self.fake.random_int(1,self.num_departements)
                    if(len(doctor_id_list) > 0):
                        generated_member["supervisor"] = doctor_id_list[self.fake.random_int(0,len(doctor_id_list))]
                    doctor_id_list.append(generated_member["id"])

                # Professor
                elif(person_type_selector == 3):
                    _staff_member_customizer(staff_member, "Professor", 35000, self.fake.random_int(31,40))
                    generated_member["table_name"] = "professor"
                    generated_member["id"] = staff_member["id"]
                    generated_member["reasearch_topic"] = self.fake.random_element(elements=self.speciality_list)
                    generated_member["surgery_participation"] = bool(self.fake.random_int(0,1))
                    generated_member["departement_id"] = self.fake.random_int(1,self.num_departements)

                # Lab Technician
                elif(person_type_selector == 4):
                    _staff_member_customizer(staff_member, "Lab Technician", 15000, self.fake.random_int(41,50))
                    generated_member["table_name"] = "lab_technician"
                    generated_member["id"] = staff_member["id"]
                    generated_member["education_level"] = self.fake.random_element(elements=["Bachelor", "Magister", "Postgraduate", "PhD"])
                    generated_member["departement_id"] = self.fake.random_int(1,self.num_departements)

                # Cleaning Team Worker
                elif(person_type_selector == 5):
                    _staff_member_customizer(staff_member, "Cleaning Team Worker", 10000, self.fake.random_int(51,55))
                    generated_member["table_name"] = "cleaning_team_worker"
                    generated_member["id"] = staff_member["id"]
                    generated_member["employment_type"] = self.fake.random_element(elements=["Part time", "Full time"])
                
                # Reseptionist
                elif(person_type_selector == 6):
                    _staff_member_customizer(staff_member, "Reseptionist", 15000, 56)
                    generated_member["table_name"] = "reseptionist"
                    generated_member["id"] = staff_member["id"]

                # Maintanence Worker
                elif(person_type_selector == 7):
                    _staff_member_customizer(staff_member, "Maintanence Worker", 15000, self.fake.random_int(57,60))
                    generated_member["table_name"] = "maintanence_worker"
                    generated_member["id"] = staff_member["id"]
                    generated_member["employment_type"] = self.fake.random_element(elements=["Part time", "Full time"])
                    generated_member["speciality"] =self.fake.random_element(elements=["Hardware", "Machines", "Furniture", "Electricity"])

                #Security Team Member
                elif(person_type_selector == 8):
                    _staff_member_customizer(staff_member, "Security Team Member", 10000, self.fake.random_int(61,63))
                    generated_member["table_name"] = "security_team_member"
                    generated_member["id"] = staff_member["id"]
                    generated_member["shifts"] = self.fake.random_element(elements=["Night", "Day"])
                    generated_member["physical_test_grade"] = self.fake.random_element(elements=["A", "B", "C", "D"])

                # HR
                elif(person_type_selector == 9):
                    _staff_member_customizer(staff_member, "HR", 30000, self.fake.random_int(64,67))
                    generated_member["table_name"] = "hr"
                    generated_member["id"] = staff_member["id"]
                    generated_member["selection_responsibility"] = self.fake.random_element(elements=["Interview", "Review"])
                
                # Pharmasist
                elif(person_type_selector == 10):
                    _staff_member_customizer(staff_member, "Pharmasist", 20000, self.fake.random_int(68,70))
                    generated_member["table_name"] = "pharmasist"
                    generated_member["id"] = staff_member["id"]
                    generated_member["education_level"] = self.fake.random_element(elements=["Bachelor", "Magister", "Postgraduate", "PhD"])
                    generated_member["research"] = bool(self.fake.random_int(0,1))
                
                # Cook
                elif(person_type_selector == 11):
                    _staff_member_customizer(staff_member, "Cook", 15000, self.fake.random_int(71,73))
                    generated_member["table_name"] = "cook"
                    generated_member["id"] = staff_member["id"]
                    generated_member["experience"] = self.fake.random_int(1,10) # At least have one year of experience after the graduation as a rule for graduation to work for one year and then they can take their certificate

                # IT Specialist
                elif(person_type_selector == 12):
                    _staff_member_customizer(staff_member, "IT Specialist", 15000, self.fake.random_int(74,77))
                    generated_member["table_name"] = "IT_specialist"
                    generated_member["id"] = staff_member["id"]
                    generated_member["support_line"] = bool(self.fake.random_int(0,1)) # At least have one year of experience after the graduation as a rule for graduation to work for one year and then they can take their certificate

                elif(person_type_selector == 13):
                    _staff_member_customizer(staff_member, "IT Specialist", 15000, self.fake.random_int(74,77))
                    generated_member["table_name"] = "IT_specialist"
                    generated_member["id"] = staff_member["id"]
                    generated_member["support_line"] = bool(self.fake.random_int(0,1)) # At least have one year of experience after the graduation as a rule for graduation to work for one year and then they can take their certificate            
            
            
        
            if(write_schema_flag):
                with open('data/person_member.sql', 'a+') as append_file:
                    # person
                    #append_file.write("\nINSERT INTO person VALUES ({:}, '{:}', '{:}', '{:}', '{:}', '{:}','{:}','{:}',{:},{:});".format(person["id"],person["first_name"], person["second_name"],person["email"],person["user_login"],person["user_password"],person["sex"],person["date_of_birth"],person["age"],person["permission_level"]))
                    self._generate_sql_schema(person,append_file)
                    if(person_type_selector == 2):
                        # patient
                        self._generate_sql_schema(patient, append_file)

                    else:
                        # staff_member
                        self._generate_sql_schema(staff_member, append_file)

                        #generated_staff_member
                        self._generate_sql_schema(generated_member, append_file)

            if(write_schema_flag):
                with open('data/contact_details.sql', 'a+') as append_file:
                    append_file.write("\nINSERT INTO contact_details VALUES ({:}, '{:}', '{:}', '{:}');".format(contact_details["id"],contact_details["phone"],contact_details["telegram"],contact_details["other"]))
        # departement
        # doc_education
        # medicine
        # meds_for_surgery
        # CCTV_rec
        # food
        # doctors_report
        # surgery
        # event
        # staff_complaint
        # patient_complaint
        # appointment
        # emergency_appointment
        # display_event
        # notification
        # invoice
        # email
        # request_med
        # request_food
        # lab
        # feedback
        # doctors_schedule
        # nurses_schedule
        # priests_schedule


        # if(write_json_flag):
        #     with open('data/person.csv', 'w') as writeFile:
        #         writer = csv.DictWriter(writeFile, fieldnames=list(person[0].keys()))
        #         writer.writeheader()
        #         for data in person:
        #             writer.writerow(data)

        #     with open('data/contact_details.csv', 'w') as writeFile:
        #         writer = csv.DictWriter(writeFile, fieldnames=list(contact_details[0].keys()))
        #         writer.writeheader()
        #         for data in contact_details:
        #             writer.writerow(data)
        
        
if __name__ == "__main__":
    db = DB()
    db.clean_schema_files()
    db.generate()
    db.pg_query("data/dep_lab.sql")
    db.pg_query("data/person_member.sql")

    # db.load_db(["person.csv","contact_details.csv"])
