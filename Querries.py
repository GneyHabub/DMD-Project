import psycopg2

class Q1:
    @staticmethod
    def execute(id):
        ids = []
        ids.append(int(id))
        con = psycopg2.connect(database="DMD", user="postgres", password="123456789", host="127.0.0.1",
                               port="5432")
        cur = con.cursor()
        cur.execute("SELECT * FROM person, doctor, appointment WHERE doctor.id = person.id AND \
                    appointment.patient_id = {:} AND\
                    (((first_name LIKE 'M%' OR first_name LIKE 'L%')\
                     OR (second_name LIKE 'M%' OR second_name LIKE 'L%')) AND \
                     (NOT ((first_name LIKE 'M%' AND second_name LIKE 'M%') \
                     OR(first_name LIKE 'L%' AND second_name LIKE 'M%')))) \
                     ORDER BY appointment.date DESC".format(ids[0]))


        rows = cur.fetchall()
        if(len(rows) == 0):
            print("No data to be shown")
        else:
            date_needed = rows[0][18]
            for row in rows:
                if(row[18] == date_needed):
                    print(row[1], row[2])


class Q2:
    @staticmethod
    def execute():
        con = psycopg2.connect(database="DMD", user="postgres", password="123456789", host="127.0.0.1",
                               port="5432")
        cur = con.cursor()
        cur.execute("SELECT doctor.id, app.time, count(*), (CAST(count(*) as FLOAT)/52), dow as app_avg \
                    FROM doctor, (SELECT *, to_char(date, 'day') as dow FROM appointment) AS app WHERE doctor.id=app.doctor_id AND \
                    app.date > current_date - interval '365 days'\
                    GROUP BY doctor.id, app.time, dow\
                    ORDER BY doctor.id, dow, app.time");

        rows = cur.fetchall()
        printed = []
        for row in rows:
            if row[0] not in printed:
                print("ID = ", row[0])
                printed.append(row[0])

            print(' Appointment day = ', row[4])
            print(" Appointment time = ", row[1])
            print(' # Appointments = ', row[2])
            print(' # Appointments AVG = ', row[3])

class Q3:
    @staticmethod
    def execute():
        con = psycopg2.connect(database="DMD", user="postgres", password="123456789", host="127.0.0.1",
                               port="5432")
        cur = con.cursor()
        cur.execute("SELECT new_id, weeks \
                    FROM(SELECT new_id, count(new_id) as weeks \
                    FROM( \
                    SELECT patient.id as new_id, week, count(*) as count_app \
                        FROM patient, (SELECT *, extract('week' from date) as week FROM appointment) AS app\
                        WHERE patient.id = app.patient_id AND \
                        app.date > current_date - interval '1 month'\
                        GROUP BY patient.id, week\
                        ORDER BY patient.id, week) AS new_table GROUP BY new_id) as new_table_2 WHERE weeks=4 ORDER BY new_id");
        #cur.execute("SELECT appointment.id FROM appointment WHERE appointment.patient_id = 261")
        rows = cur.fetchall()
        printed = []
        for row in rows:
            print("ID = ", row[0])

class Q4:
    @staticmethod
    def execute():
        con = psycopg2.connect(database="DMD", user="postgres", password="123456789", host="127.0.0.1",
                               port="5432")
        cur = con.cursor()
        cur.execute("SELECT sum(person_charge_2.charge) \
                    FROM\
                    (SELECT person_charge.patient_id as id, person_charge.age as age, person_charge.app_num as app_num, CAST(\
                        CASE \
                            WHEN (person_charge.age < 50) AND (person_charge.app_num < 3) \
                                THEN 200\
                            WHEN (person_charge.age < 50) AND (person_charge.app_num >= 3) \
                                THEN 250\
                            WHEN (person_charge.age >= 50) AND (person_charge.app_num < 3) \
                                THEN 400\
                            WHEN (person_charge.age >= 50) AND (person_charge.app_num >= 3) \
                                THEN 500\
                        END AS float) as charge \
                    FROM \
                    (SELECT patient.id as patient_id, person.age as age, count(patient.id) as app_num \
                            FROM patient, appointment, person\
                            WHERE patient.id = appointment.patient_id AND patient.id = person.id AND \
                                  appointment.date BETWEEN current_date - interval '2 month' AND\
                            current_date - interval '1 month' \
                            GROUP BY patient.id, person.age\
                            ORDER BY patient.id) AS person_charge) AS person_charge_2, appointment WHERE \
                    appointment.patient_id = person_charge_2.id");
        rows = cur.fetchall()
        for row in rows:
            print("Income = ", row[0])

class Q5:
    @staticmethod
    def execute():
        con = psycopg2.connect(database="DMD", user="postgres", password="123456789", host="127.0.0.1",
                               port="5432")
        cur = con.cursor()
        cur.execute("SELECT new_table_2.id \
                    FROM\
                        (SELECT new_table.id, sum(app_per_year) as total\
                        FROM \
                        (SELECT doctor.id as id, count(*) as app_per_year, year \
                                FROM doctor, (SELECT *, extract('year' from date) as year FROM appointment) AS app WHERE doctor.id=app.doctor_id AND \
                                app.date > current_date - interval '10 years' - interval '1' day * extract('DOY' from current_date)\
                                GROUP BY doctor.id, year\
                                ORDER BY doctor.id, year) as new_table \
                        WHERE app_per_year > 5 GROUP BY new_table.id) as new_table_2 \
                    WHERE total > 100");

        rows = cur.fetchall()
        printed = []
        for row in rows:
            if row[0] not in printed:
                print("ID = ", row[0])
                printed.append(row[0])
