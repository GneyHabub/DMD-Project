import psycopg2
from psycopg2 import Error
from faker import Faker
import json
import csv
import numpy as np
from datetime import date
from datetime import timedelta
from tqdm import tqdm

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x):
        return x


class Hospital:
    def __init__(self,user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432", database = "DMD"):
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
        
        # Source: https://www.stjude.org/treatment/patient-resources/caregiver-resources/medicines/a-z-list-of-medicines.html
        self.medicine_list = ["Abacavir", "Acyclovir", "Alemtuzumab", "Alendronate", "Allopurinol"
                            , "Amifostine", "Amikacin", "Aminocaproic Acid", "Amitriptyline", "Amlodipine", "Amoxicillin"
                            , "Aprepitant", "Asparaginase", "Atazanavir", "Atenolol", "Atovaquone", "Azithromycin", "Baclofen"
                            , "Bleomycin", "Bortezomib", "Bosentan", "Busulfan", "Calcium", "Captopril", "Carbamazepine", "Carboplatin"
                            , "Carmustine", "Cefaclor", "Cefepime", "Cefixime", "Ceftazidime", "Cefuroxime", "Celecoxib", "Cephalexin"
                            , "Cidofovir", "Cisplatin", "Cladribine", "Clarithromycin", "Clindamycin", "Clobazam", "Clofarabine", "Codeine"
                            , "Crizotinib", "Cyclobenzaprine", "Cyclophosphamide", "Cyclosporine", "Cyproheptadine", "Cytarabine", "Dacarbazine"
                            , "Dactinomycin", "Dapsone", "Darunavir", "Dasatinib", "Daunorubicin", "Deferasirox", "Desmopressin", "Dexamethasone", "Diclofenac"
                            , "Didanosine", "Dinutuximab", "Dobutamine", "Dopamine", "Dornase alfa", "Doxorubicin", "Dronabinol", "Efavirenz", "Eltrombopag", "Elvitegravir"
                            , "Emicizumab", "Emtricitabine", "Enalapril", "Enoxaparin", "Erlotinib", "Erythromycin", "Erythropoietin", "Etonogestrel", "Etoposide"
                            , "Etravirine", "Famciclovir", "Fluconazole", "Fludarabine", "Fluorouracil", "Foscarnet", "Furosemide", "G-CSF", "Gabapentin"
                            , "Ganciclovir", "Gefitinib", "Gemcitabine", "Gemtuzumab", "GM-CSF", "Granisetron", "Heparin", "Hydralazine"
                            , "Hydrocodone", "Hydrocortisone", "Hydromorphone", "Hydroxyurea", "Ifosfamide", "Imatinib", "Imipenem", "Immune"
                            , "Interferon", "Interleukin", "Irinotecan", "Isotretinoin", "Itraconazole", "Ketoconazole", "L-glutamine", "Labetalol"
                            , "Lamivudine", "Leucovorin", "Levothyroxine", "Linezolid", "Lomustine", "Lopinavir", "Lorazepam", "Magnesium", "Maraviroc", "Mechlorethamine"
                            , "Megestrol acetate", "Meloxicam", "Melphalan", "Meperidine", "Mercaptopurine", "Meropenem", "Mesna", "Methadone"
                            , "Methotrexate", "Methylphenidate", "Metronidazole", "Micafungin", "Mitotane", "Mitoxantrone", "Modafinil", "Morphine", "Muromonab"
                            , "Mycophenolate", "Nelarabine", "Nelfinavir", "Neuromuscular", "Nevirapine", "Norepinephrine", "Omeprazole", "Ondansetron"
                            , "Oxycodone", "Paclitaxel", "PEGaspargase", "Pegfilgrastim", "Pemetrexed", "Penicillin", "Pentamidine", "Phenobarbital", "Phenytoin"
                            , "Phosphorus", "Posaconazole", "Potassium", "Prednisone", "Probenecid", "Procarbazine", "Promethazine", "Propoxyphene", "Raltegravir"
                            , "Ranitidine", "Rasburicase", "Rilpivirine", "Ritonavir", "Rituximab", "Rivaroxaban", "Ruxolitinib", "Saquinavir", "Sirolimus"
                            , "Sorafenib", "Stavudine", "Sucralfate", "Sugammadex", "Sunitinib", "Tacrolimus", "Temozolomide", "Teniposide", "Tenofovir", "Thioguanine"
                            , "Thiotepa", "Tobramycin", "Topotecan", "Tretinoin", "Trimethoprim", "Valproic acid", "Vancomycin", "Vinblastine", "Vincristine"
                            , "Voriconazole", "Vorinostat", "Warfarin", "Zidovudine"]
        
        # Source: http://eatingatoz.com/food-list/
        self.food_list = ["asparagus", "apples", "avacado", "alfalfa", "almond", "arugala", "artichoke", "applesauce", "noodles", "antelope", "tuna", "Apple juice", "Avocado roll", "Bruscetta", "bacon", "black beans", "bagels"
                        , "baked beans", "BBQ", "bison", "barley", "beer", "bisque", "bluefish", "bread", "broccoli", "buritto", "babaganoosh", "Cabbage", "cake", "carrots", "carne asada", "celery", "cheese", "chicken", "catfish", "chips", "chocolate"
                        , "chowder", "clams", "coffee", "cookies", "corn", "cupcakes", "crab", "curry", "cereal", "chimichanga", "dates", "dips", "duck", "dumplings", "donuts", "eggs", "enchilada", "eggrolls", "English muffins", "edimame", "sushi", "fajita"
                        , "falafel", "fish", "franks", "fondu", "French dip", "Garlic", "ginger", "gnocchi", "goose", "granola", "grapes", "green beans", "Guancamole", "gumbo", "grits", "Graham crackers", "ham", "halibut", "hamburger", "honey", "huenos rancheros"
                        , "hash browns", "hot dogs", "haiku roll", "hummus", "ice cream", "Irish stew", "Indian food", "Italian bread", "jambalaya", "jelly", "jerky", "jalapeño", "kale", "kabobs", "ketchup", "kiwi", "kidney beans", "kingfish", "lobster", "Lamb", "Linguine", "Lasagna"
                        , "Meatballs", "Moose", "Milk", "Milkshake", "Noodles", "Ostrich", "Pizza", "Pepperoni", "Porter", "Pancakes", "Quesadilla", "Quiche", "Reuben", "Spinach", "Spaghetti", "Tater tots", "Toast", "Venison", "Waffles", "Wine", "Walnuts", "Yogurt", "Ziti", "Zucchini"]
        
        self.valid_patient_id = []
        self.valid_doctor_id = []
        self.valid_staff_id = []
        self.valid_IT_id = []
        self.valid_maintanence_id = []
        self.valid_nurse_id = []
        self.valid_priest_id = []

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
            
    def generate(self):
        self._generate_facilities()
        self._generate_person_member_db()
        self._generate_appointment_db()
        self._generate_complaint_db()
        self._generate_medicine_surgery_db()
        self._generate_events_other_db()
        self._generate_feedback_db()
        self._generate_schedule_db()
    
    def clean_schema_files(self):
        f = open('data/dep_lab.sql', 'w')
        f.close()
        f = open('data/person_member.sql', 'w')
        f.close()
        f = open('data/contact_details.sql', 'w')
        f.close()
        f = open('data/appointment.sql', 'w')
        f.close()
        f = open('data/complaint.sql', 'w')
        f.close()
        f = open('data/medicine_surgery.sql', 'w')
        f.close()
        f = open('data/events_other.sql', 'w')
        f.close()
        f = open('data/feedback.sql', 'w')
        f.close()
        f = open('data/schedule.sql', 'w')
        f.close()
        f = open('data/appointment_q3_sick.sql', 'w')
        f.close()



    def _generate_sql_schema(self, object, append_file):
        generation_string_header = "\nINSERT INTO {:} (".format(object["table_name"])
        generation_string_values = "VALUES ("
        for i in object.keys():
            if(i == "table_name"):
                continue
            generation_string_header += "{:},".format(i)
            if(type(object[i]) == str):
                generation_string_values += "'{:}',".format(object[i])
            elif(type(object[i]) == bool):
                generation_string_values += "B'{:}',".format(int(object[i]))

            else:
                generation_string_values += "{:},".format(object[i])
            
        generation_string = generation_string_header[:-1] + ") " + generation_string_values[:-1] + ");"
        
        append_file.write(generation_string)

    def _generate_facilities(self, write_schema_flag=True, write_json_flag=False):
        valid_departement_list = self.fake.random_elements(elements=self.departement_list,length=self.num_departements,unique=True)
        num_labs_dep = self.fake.random_int(1,3)
        lab_list = []       
        for i in range(self.num_departements):
            departement = {"table_name": "departement", "id":i+1, "name": valid_departement_list[i][:30]}
            labs = []
            for x in range(num_labs_dep):
                labs.append({"table_name": "lab", "id": (i)*3+(x+1), "name": valid_departement_list[i][:25]+" lab"+str(x+1), "departement_id": i+1})
                lab_list.append(valid_departement_list[i]+" lab"+str(x+1))
            
            if(write_schema_flag):
                with open('data/dep_lab.sql', 'a+') as append_file:
                    self._generate_sql_schema(departement,append_file)
                    for lab in labs:
                        self._generate_sql_schema(lab, append_file)

    def _generate_person_member_db(self, num=500, write_schema_flag=True, write_json_flag=False):
        # using the property of aliasing and nested functions
        def _staff_member_customizer(staff_member, position, salary, room):
            staff_member["position"] = position
            staff_member["salary"] = salary
            staff_member["room"] = room

        # person = []
        # contact_details = []
        # staff_member = []
        print("Generate person_member.sql")
        for i in tqdm(range(0, num)):
            # person.append({})
            # contact_details.append({})
            person = {"table_name":"person"}
            contact_details = {}
            staff_member = {"table_name": "staff_member"}
            generated_member = {}
            patient = {"table_name":"patient"}
            patient_address = {"table_name":"patients_address"}
            medical_history = {"table_name": "medical_history"}
            languages_spoken = {"table_name":"languages_spoken"}

            profile = self.fake.profile()
            person["id"]= i+1
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
            contact_details["telegram"] = "@"+profile["username"][:30]
            contact_details["other"] = "".join(self.fake.random_letters(length=30) if i%5 else "")
            
            # IT_complaint


            #reseptionist, maintanence_worker, cleaning_team_worker, security_team_member, hr, pharmasist,
            # cook, priest, nurse, IT_specialist, prof, doctor, patient, lab_technician
            person_type_selector = np.random.choice(14,1,p=[0.2,0.15,0.2,0.1,0.05,0.05,0.05,0.05,0.02,0.03,0.03,0.03,0.02,0.02])
            if(person_type_selector == 2):
                patient["id"] = person["id"]
                staff_member["registration_date"] = str(self.fake.date_between(start_date="-40d", end_date="today")) 
                staff_member["occupation"] = profile["job"][:50]
                patient_address["street"] = self.fake.name().split(" ")[0][:26]+" st."
                patient_address["house"] = str(self.fake.random_int(1,100))
                patient_address["apartement"] = str(self.fake.random_int(1,10))
                self.valid_patient_id.append(patient["id"])
                medical_history["patient_id"] = patient["id"]
                medical_history["date"] = str(self.fake.date_between(start_date="-40d", end_date="today"))
                
            else:
                # staff_member
                staff_member["id"] = person["id"]
                staff_member["employed_since"] = str(self.fake.date_between(start_date="-10y", end_date="today"))
                self.valid_staff_id.append(staff_member["id"])
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
                    self.valid_nurse_id.append(generated_member["id"])

                # Doctor
                elif(person_type_selector == 1):
                    _staff_member_customizer(staff_member, "Doctor", 35000, self.fake.random_int(11,30))
                    generated_member["table_name"] = "doctor"
                    generated_member["id"] = staff_member["id"]
                    generated_member["speciality"] = self.fake.random_element(elements=self.speciality_list)
                    generated_member["emergency_hours"] = bool(self.fake.random_int(0,1))
                    generated_member["experience"] = self.fake.random_int(1,10) # At least have one year of experience after the graduation as a rule for graduation to work for one year and then they can take their certificate
                    generated_member["departement_id"] = self.fake.random_int(1,self.num_departements)
                    if(len(self.valid_doctor_id) > 0):
                        generated_member["supervisor"] = self.valid_doctor_id[self.fake.random_int(0,len(self.valid_doctor_id)-1)]
                    self.valid_doctor_id.append(generated_member["id"])

                # Professor
                elif(person_type_selector == 3):
                    _staff_member_customizer(staff_member, "Professor", 35000, self.fake.random_int(31,40))
                    generated_member["table_name"] = "professor"
                    generated_member["id"] = staff_member["id"]
                    generated_member["research_topic"] = self.fake.random_element(elements=self.speciality_list)
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
                    languages_spoken["reseptionist_id"] = generated_member["id"]
                    languages_spoken["language"] = "".join(self.fake.random_elements(elements=["English", "Russian", "Arabic", "Tatar", "Italian", "Portugues"]))
                
                # Maintanence Worker
                elif(person_type_selector == 7):
                    _staff_member_customizer(staff_member, "Maintanence Worker", 15000, self.fake.random_int(57,60))
                    generated_member["table_name"] = "maintanence_worker"
                    generated_member["id"] = staff_member["id"]
                    generated_member["employment_type"] = self.fake.random_element(elements=["Part time", "Full time"])
                    generated_member["speciality"] =self.fake.random_element(elements=["Hardware", "Machines", "Furniture", "Electricity"])
                    self.valid_maintanence_id.append(generated_member["id"])

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
                    generated_member["support_line"] = bool(self.fake.random_int(0,1))
                    self.valid_IT_id.append(generated_member["id"])

                # Priest
                elif(person_type_selector == 13):
                    _staff_member_customizer(staff_member, "Priest", 15000, self.fake.random_int(78,80))
                    generated_member["table_name"] = "priest"
                    generated_member["id"] = staff_member["id"]
                    generated_member["religion"] = self.fake.random_element(elements=["Judaism", "Christianity", "Islam"])
                    self.valid_priest_id.append(generated_member["id"])

                elif(person_type_selector == 14):
                    _staff_member_customizer(staff_member, "Doctor Education", 30000, self.fake.random_int(81,85))
                    generated_member["table_name"] = "doc_education"
                    generated_member["id"] = staff_member["id"]
                    generated_member["university"] = self.fake.random_element(elements=["Harvard", "Columbia", "Stanford", "Moscow", "Oxford", "AURO", "Bacu", "Kazan"])
                    generated_member["graduated"] = str(self.fake.date_between(start_date="-10y", end_date="today")) 
                    generated_member["degree"] = self.fake.random_element(elements=["Bachelor", "Magister", "PhD"])

            if(write_schema_flag):
                with open('data/person_member.sql', 'a+') as append_file:
                    # person
                    #append_file.write("\nINSERT INTO person VALUES ({:}, '{:}', '{:}', '{:}', '{:}', '{:}','{:}','{:}',{:},{:});".format(person["id"],person["first_name"], person["second_name"],person["email"],person["user_login"],person["user_password"],person["sex"],person["date_of_birth"],person["age"],person["permission_level"]))
                    self._generate_sql_schema(person,append_file)
                    if(person_type_selector == 2):
                        # patient
                        self._generate_sql_schema(patient, append_file)
                        self._generate_sql_schema(patient_address, append_file)
                        self._generate_sql_schema(medical_history, append_file)

                    else:
                        # staff_member
                        self._generate_sql_schema(staff_member, append_file)

                        #generated_staff_member
                        self._generate_sql_schema(generated_member, append_file)
                        
                        if(person_type_selector == 6 and i > 1):
                            self._generate_sql_schema(languages_spoken, append_file)
            
            if(write_schema_flag):
                with open('data/contact_details.sql', 'a+') as append_file:
                    append_file.write("\nINSERT INTO contact_details VALUES ({:}, '{:}', '{:}', '{:}');".format(contact_details["id"],contact_details["phone"],contact_details["telegram"],contact_details["other"]))

    # appointment and doctors_reports
    def _generate_appointment_db(self, num=10000, write_schema_flag=True, write_json_flag=False):
        print("Generate appointment.sql")
        for i in tqdm(range(num)):
            time = "{:02d}:{:02d}:{:02d}".format(self.fake.random_int(9,18),15*self.fake.random_int(0,3),0)
            appointment = {"table_name": "appointment", "id":i+1, "time":time, "date": str(self.fake.date_between(start_date="-12y",end_date="+20d")), "patient_id": self.fake.random_element(elements=self.valid_patient_id), "doctor_id": self.fake.random_element(elements=self.valid_doctor_id)}
            if(write_schema_flag):
                with open('data/appointment.sql', 'a+') as append_file:
                    self._generate_sql_schema(appointment, append_file)
        self._generate_sick_patient_db(num)
        print("Continue generation appointment.sql")
        for i in tqdm(range(num//10)):
            time = "{:02d}:{:02d}:{:02d}".format(self.fake.random_int(9,18),15*self.fake.random_int(0,3),0)
            date = self.fake.date_between(start_date="-12y",end_date="+20d")
            appointment = {"table_name": "emergency_appointment", "id":i+1, "time":time, "date": str(date), "patient_id": self.fake.random_element(elements=self.valid_patient_id), "doctor_id": self.fake.random_element(elements=self.valid_doctor_id)}
            if(write_schema_flag):
                with open('data/appointment.sql', 'a+') as append_file:
                    self._generate_sql_schema(appointment, append_file)
                    if(date < date.today()):
                        doctors_report = {"table_name": "doctors_report", "appointment_id": i+1, "text":self.fake.text()}
                        self._generate_sql_schema(doctors_report, append_file)

    def _generate_sick_patient_db(self,start_id, num=10, write_schema_flag=True, write_json_flag=False):
        counter = start_id+1
        for i in tqdm(range(num//3)):
            time = "{:02d}:{:02d}:{:02d}".format(self.fake.random_int(9,18),15*self.fake.random_int(0,3),0)
            patient_id = self.fake.random_element(elements=self.valid_patient_id)
            for x in range(4):
                date = "{:04d}-{:02d}-{:02d}".format(2019,11,(x)*7+self.fake.random_int(1,6))
                appointment1 = {"table_name": "appointment", "id":counter, "time":time, "date": date, "patient_id": patient_id, "doctor_id": self.fake.random_element(elements=self.valid_doctor_id)}
                date = "{:04d}-{:02d}-{:02d}".format(2019,11,(x)*7+self.fake.random_int(1,6))
                counter += 1
                appointment2 = {"table_name": "appointment", "id":counter, "time":time, "date": date, "patient_id": patient_id, "doctor_id": self.fake.random_element(elements=self.valid_doctor_id)}
                counter += 1
                if(write_schema_flag):
                    with open('data/appointment_q3_sick.sql', 'a+') as append_file:
                        self._generate_sql_schema(appointment1, append_file)
                        self._generate_sql_schema(appointment2, append_file)



    def _generate_complaint_db(self, num=1000, write_schema_flag=True, write_json_flag=False):
        print("Generate complaint.sql")
        for i in tqdm(range(num)):
            selector = self.fake.random_int(1,3)
            complaint = {"table_name":"", "id": i, "submitted":str(self.fake.date_between(start_date="-5d",end_date="today")), "resolved":str(self.fake.date_between(start_date="-5d",end_date="today")), "subjectr": self.fake.text()}
            # patient_complaint
            if(selector == 1):
                complaint["table_name"] = "patient_complaint"
                complaint["patient_id"] = self.fake.random_element(elements=self.valid_patient_id)
            # IT_complaint
            elif(selector == 2):
                complaint["table_name"] = "IT_complaint"
                complaint["person_id"] = self.fake.random_element(elements=self.valid_patient_id+self.valid_staff_id)
                complaint["responsible"] = self.fake.random_element(elements=self.valid_IT_id)
            # staff_complaint
            elif(selector == 3):
                complaint["table_name"] = "staff_complaint"
                complaint["staff_id"] = self.fake.random_element(elements=self.valid_staff_id)
                complaint["responsible"] = self.fake.random_element(elements=self.valid_maintanence_id)
            
            if(write_schema_flag):
                with open('data/complaint.sql', 'a+') as append_file:
                    self._generate_sql_schema(complaint, append_file)

    def _generate_medicine_surgery_db(self, num=3000, write_schema_flag=True, write_json_flag=False):
        valid_medicine = self.fake.random_elements(elements=self.medicine_list, length=min(num+60,len(self.medicine_list)), unique=True)
        print("Generate medicine_surgery.sql")
        for i in tqdm(range(min(num+60,len(self.medicine_list)))):
            medicine = {"table_name": "medicine", "name":valid_medicine[i], "amount": self.fake.random_int(0,100)}
            if(write_schema_flag):
                with open('data/medicine_surgery.sql', 'a+') as append_file:
                    self._generate_sql_schema(medicine, append_file)
                    if(self.fake.random_int(0,1) == 1):
                        request_med = {"table_name": "request_med", "date": str(self.fake.date_between(start_date="-5d",end_date="+30d")), "med":medicine["name"], "amount": self.fake.random_int(1,10), "requester":self.fake.random_element(elements=self.valid_staff_id)} 
                        self._generate_sql_schema(request_med, append_file)
                        patient_allergies = {"table_name": "patient_allergies", "patient_id":self.fake.random_element(elements=self.valid_patient_id), "preparate":medicine["name"]}
                        self._generate_sql_schema(patient_allergies, append_file)
        
        print("Continue Generate medicine_surgery.sql")
        for i in range(num):
            surgery = {"table_name": "surgery", "id": i+1, "date":str(self.fake.date_between(start_date="-5d",end_date="+30d")), "patient_id":self.fake.random_element(elements=self.valid_patient_id), "doctor_id": self.fake.random_element(elements=self.valid_doctor_id)}
            meds_surgery = {"table_name": "meds_for_surgery", "surgery_id": i+1, "med":self.fake.random_element(elements=valid_medicine)}
            if(write_schema_flag):
                with open('data/medicine_surgery.sql', 'a+') as append_file:
                    self._generate_sql_schema(surgery, append_file)
                    self._generate_sql_schema(meds_surgery, append_file)

    # event, staff_meeting, invited, display_event, notification, email, invoice, CCTV_rec, food,
    def _generate_events_other_db(self, num=5000, write_schema_flag=True, write_json_flag=False):
        valid_food = self.fake.random_elements(elements=self.food_list, length=min(num,len(self.food_list)), unique=True)
        initial_date = self.fake.date_between(start_date="-{:}d".format(num),end_date="+{:}d".format(num))
        valid_dates = [initial_date+timedelta(days=i) for i in range(num)]

        print("Generate events_other.sql")
        for i in tqdm(range(min(num,len(self.food_list)))):
            food = {"table_name": "food", "name":valid_food[i][:30], "amount": self.fake.random_int(0,100), "supplier": self.fake.company()[:30], "can_be_allergic": bool(self.fake.random_int(0,1))}
            if(write_schema_flag):
                with open('data/events_other.sql', 'a+') as append_file:
                    self._generate_sql_schema(food, append_file)
                    if(self.fake.random_int(0,1) == 1):
                        request_food = {"table_name": "request_food", "food":food["name"], "amount": self.fake.random_int(1,10)} 
                        self._generate_sql_schema(request_food, append_file)
        
        print("Continue Generate events_other.sql")
        for i in tqdm(range(num)):
            meeting_date = str(valid_dates[i])
            staff_meeting = {"table_name": "staff_meeting", "date": meeting_date, "topic": self.fake.text()[:30]}
            invited = {"table_name": "invited", "staff_member_id":self.fake.random_element(elements=self.valid_staff_id), "meeting":meeting_date}
            CCTV_rec = {"table_name": "CCTV_rec", "date":str(valid_dates[i]), "camera_num": self.fake.random_int(1,100)} 
            event = {"table_name": "event", "id": i+1, "title":self.fake.text()[:40]}
            display_event = {"table_name": "display_event", "person": self.fake.random_element(elements=self.valid_staff_id+self.valid_patient_id), "event": self.fake.random_int(1,i+1)}
            notification = {"table_name": "notification", "person_id": self.fake.random_element(elements=self.valid_staff_id+self.valid_patient_id), "topic":self.fake.text()[:40]}
            invoice = {"table_name": "invoice", "id": i+1, "date":str(self.fake.date_between(start_date="-5d",end_date="+30d")), "amount": self.fake.random_int(100,100000), "subject":self.fake.text(), "debtor": self.fake.random_element(elements=self.valid_staff_id+self.valid_patient_id)}
            email = {"table_name":"email","date":str(self.fake.date_between(start_date="-5d",end_date="+30d")), "sent": self.fake.random_element(elements=self.valid_staff_id+self.valid_patient_id), "recived":self.fake.random_element(elements=self.valid_staff_id+self.valid_patient_id)}
            if(write_schema_flag):
                with open('data/events_other.sql', 'a+') as append_file:
                    self._generate_sql_schema(staff_meeting, append_file)
                    self._generate_sql_schema(invited, append_file)
                    self._generate_sql_schema(CCTV_rec, append_file)
                    self._generate_sql_schema(event, append_file)
                    self._generate_sql_schema(display_event, append_file)
                    self._generate_sql_schema(notification, append_file)
                    self._generate_sql_schema(invoice, append_file)
                    self._generate_sql_schema(email, append_file)

    # request_med, request_food, feedback
    def _generate_feedback_db(self, num=5000, write_schema_flag=True, write_json_flag=False):
        
        print("Generate feedback.sql")
        for i in tqdm(range(num)):
            feedback = {"table_name": "feedback", "patient_id": self.fake.random_element(elements=self.valid_patient_id), "doctor_id": self.fake.random_element(elements=self.valid_doctor_id), "text": self.fake.text()}
            
            if(write_schema_flag):
                with open('data/feedback.sql', 'a+') as append_file:
                    self._generate_sql_schema(feedback, append_file)

    # doctors_schedule, nurses_schedule, priests_schedule
    def _generate_schedule_db(self, num=1000, write_schema_flag=True, write_json_flag=False):
        
        print("Generate schedule.sql")
        for i in tqdm(range(num)):
            selector = self.fake.random_int(1,3)
            schedule = {"table_name":"", "date":str(self.fake.date_between(start_date="-5d",end_date="+5d"))}
            # doctors_schedule
            if(selector == 1):
                schedule["table_name"] = "doctors_schedule"
                schedule["nurse_id"] = self.fake.random_element(elements=self.valid_nurse_id)
                schedule["doctor_id"] = self.fake.random_element(elements=self.valid_doctor_id)

            # nurses_schedule
            elif(selector == 2):
                schedule["table_name"] = "nurses_schedule"
                schedule["nurse_id"] = self.fake.random_element(elements=self.valid_nurse_id)
                schedule["shift"] = self.fake.random_element(elements=["Night", "Day"])
            # priests_schedule
            elif(selector == 3):
                schedule["table_name"] = "priests_schedule"
                schedule["patient_id"] = self.fake.random_element(elements=self.valid_patient_id)
                schedule["priest_id"] = self.fake.random_element(elements=self.valid_priest_id)
            if(write_schema_flag):
                with open('data/schedule.sql', 'a+') as append_file:
                    self._generate_sql_schema(schedule, append_file)

        # doctors_schedule
        # nurses_schedule
        # priests_schedule


        
if __name__ == "__main__":
    db = Hospital(database="DMD")
    db.clean_schema_files()
    db.generate()
    db.pg_query("data/dep_lab.sql")
    db.pg_query("data/person_member.sql")
    db.pg_query("data/contact_details.sql")
    db.pg_query("data/appointment.sql")
    db.pg_query("data/complaint.sql")
    db.pg_query("data/medicine_surgery.sql")
    db.pg_query("data/events_other.sql")
    db.pg_query("data/feedback.sql")
    db.pg_query("data/schedule.sql")
    db.pg_query("data/appointment_q3_sick.sql")

