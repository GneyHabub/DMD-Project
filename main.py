from DB import Hospital
import Querries

db = Hospital(database="DMD")
db.pg_query("data/dep_lab.sql")
db.pg_query("data/person_member.sql")
db.pg_query("data/contact_details.sql")
db.pg_query("data/appointment.sql")
db.pg_query("data/complaint.sql")
db.pg_query("data/medicine_surgery.sql")
db.pg_query("data/events_other.sql")
db.pg_query("data/feedback.sql")
db.pg_query("data/schedule.sql")  

print("Commands:\n\
      0 --> Exit\n\
      1 -- 5 --> Query num. \n\
      c --> Clear and generate new dataset")

while(True):
    querry = input("Type the number of query you wish to execute or 0 in order to exit:")
    if querry=='1':
        Querries.Q1.execute()
    elif querry=='2':
        Querries.Q2.execute()
    elif querry=='3':
        Querries.Q3.execute()
    elif querry=='4':
        Querries.Q4.execute()
    elif querry=='5':
        Querries.Q5.execute()
    elif querry=='0':
        break

    elif querry == 'c':
        print("Clear and generate new dataset")
        db.pg_query("schema.sql")
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

    else:
        print("You input was not recognized, please try again")


