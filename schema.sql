
-- If u find any misspelling, just fix it
-- If u find any incosistency or bag, just fix it)
-- In oreder to run this file, you need to drop every table and then create again,
-- that's why here is this big block of drops))))))

DROP TABLE IF EXISTS emergency_appointment;
DROP TABLE IF EXISTS doctors_schedule;
DROP TABLE IF EXISTS nurses_schedule;
DROP TABLE IF EXISTS priests_schedule;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS surgery;
DROP TABLE IF EXISTS meds_for_surgery;
DROP TABLE IF EXISTS doctors_report;
DROP TABLE IF EXISTS medical_history;
DROP TABLE IF EXISTS staff_meeting;
DROP TABLE IF EXISTS CCTV_rec;
DROP TABLE IF EXISTS invoice;
DROP TABLE IF EXISTS email;
DROP TABLE IF EXISTS request_med;
DROP TABLE IF EXISTS request_food;
DROP TABLE IF EXISTS lab;
DROP TABLE IF EXISTS medicine;
DROP TABLE IF EXISTS contact_details;
DROP TABLE IF EXISTS head_doctor;
DROP TABLE IF EXISTS reseptionist;
DROP TABLE IF EXISTS cleaning_team_worker;
DROP TABLE IF EXISTS security_team_member;
DROP TABLE IF EXISTS hr;
DROP TABLE IF EXISTS pharmasist;
DROP TABLE IF EXISTS cook;
DROP TABLE IF EXISTS priest;
DROP TABLE IF EXISTS head_nurse;
DROP TABLE IF EXISTS nurse;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS doc_education;
DROP TABLE IF EXISTS patients_address;
DROP TABLE IF EXISTS lab_technician;
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS patient_complaint;
DROP TABLE IF EXISTS IT_complaint;
DROP TABLE IF EXISTS staff_complaint;
DROP TABLE IF EXISTS maintanence_worker;
DROP TABLE IF EXISTS IT_specialist;
DROP TABLE IF EXISTS staff_member;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS departement;
DROP TABLE IF EXISTS notification;
DROP TABLE IF EXISTS display_event;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS person;

CREATE TABLE person(
    id INT PRIMARY KEY NOT NULL UNIQUE,
    full_name VARCHAR(50) NOT NULL, -- Supposed to ba composite, but SQL doesn't support it, so let it be just a string
    email VARCHAR(50),
    user_login VARCHAR(30) NOT NULL default 'login',
    user_password VARCHAR(30) NOT NULL default '12345',
    sex VARCHAR(1) NOT NULL,
    date_of_birth DATE,
    age INT NOT NULL,
    permission_level INT NOT NULL default 0
);

CREATE TABLE contact_details(
    id INT,
    FOREIGN KEY(id) REFERENCES person(id),
    phone VARCHAR(20),
    telegram VARCHAR(30),
    other VARCHAR(50)
);

CREATE TABLE staff_member(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    position VARCHAR(20),
    salary INT NOT NULL,
    working_hours VARCHAR,
    employed_since DATE NOT NULL,
    room VARCHAR(10)
);

CREATE TABLE departement(
    id INT PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE head_doctor(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    primary_speciality VARCHAR(20)
);

CREATE TABLE reseptionist(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    spoken_languages VARCHAR(100) default 'English' -- The same as in full name. 
    -- We either crewate a new table, or just make it string.
);

CREATE TABLE maintanence_worker(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    employment_type VARCHAR(9) NOT NULL, -- Strictly 'Part time' or 'Full time' only
    speciality VARCHAR(100) -- Composite again
);

CREATE TABLE cleaning_team_worker(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    employment_type VARCHAR(9) -- Strictly 'Part time' or 'Full time' only
);

CREATE TABLE security_team_member(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    shifts VARCHAR(5) NOT NULL, -- 'Night' or 'Day' only
    physical_test_grade VARCHAR(1) -- A, B, C or D
);

CREATE TABLE hr(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    selection_responsibility VARCHAR(10)-- Strictly 'Interview' or 'Review' only
);

CREATE TABLE pharmasist(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    education_level VARCHAR (15), -- 'Bachelor', 'Magister', 'Postgraduate', 'PhD'
    reasearch BIT NOT NULL-- Analogus to Boolean. 1 - True, 0 - False
);

CREATE TABLE cook(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    experience INT -- Years
);

CREATE TABLE priest(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    religion VARCHAR(15)
);

CREATE TABLE head_nurse(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    surgery_assistant BIT NOT NULL -- Whether or not he/she sometimes assist in surgeries
);

CREATE TABLE nurse(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    surgery_assistant BIT NOT NULL, -- Whether or not he/she sometimes assist in surgeries
    preferred_shifts VARCHAR(5), -- 'Night' or 'Day' only
    appointment_assistant BIT NOT NULL, -- Whether or not he/she sometimes assist during appointments
    departement_id INT,
    FOREIGN KEY (departement_id) REFERENCES departement(id)
);

CREATE TABLE IT_specialist(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    support_line BIT NOT NULL
);

CREATE TABLE professor(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    reasearch_topic VARCHAR(50),
    surgery_participation BIT NOT NULL,
    departement_id INT,
    FOREIGN KEY (departement_id) REFERENCES departement(id)
);

CREATE TABLE doctor(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    speciality VARCHAR(30),
    emergency_hours BIT NOT NULL, -- Has them or not
    experience INT default 0, -- Number of years in the industry
    departement_id INT,
    supervisor INT,
    FOREIGN KEY (departement_id) REFERENCES departement(id),
    FOREIGN KEY (supervisor) REFERENCES doctor(id)
);

CREATE TABLE doc_education(
    id INT,
    FOREIGN KEY(id) REFERENCES doctor(id),
    university VARCHAR(30),
    graduated DATE,
    degree VARCHAR (10) -- 'Bachelor', 'Magister', 'PhD'
);

CREATE TABLE patient(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    registration_date DATE NOT NULL default now(),
    allergies TEXT, -- multivalued
    occupation VARCHAR(50)
);

CREATE TABLE patients_address(
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    country VARCHAR(30) default 'Russian Federation',
    district VARCHAR(40) default 'Tatarstan',
    city VARCHAR(20) default 'Innopolis',
    street VARCHAR(30),
    house VARCHAR(8),
    apartement VARCHAR(8)
);

CREATE TABLE lab_technician(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    education_level VARCHAR (15), -- 'Bachelor', 'Magister', 'Postgraduate', 'PhD'
    departement_id INT,
    FOREIGN KEY (departement_id) REFERENCES departement(id)
);

CREATE TABLE appointment(
    id INT PRIMARY KEY,
    time TIME,
    date DATE,
    patient_id INT,
    doctor_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

CREATE TABLE patient_complaint(
    id INT PRIMARY KEY,
    submitted DATE,
    resolved DATE,
    subjectr TEXT,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);

CREATE TABLE IT_complaint(
    id INT PRIMARY KEY,
    submitted DATE,
    resolved DATE,
    subjectr TEXT,
    person_id INT,
    responsible INT,
    FOREIGN KEY (person_id) REFERENCES person(id),
    FOREIGN KEY (responsible) REFERENCES IT_specialist(id)
);

CREATE TABLE staff_complaint(
    id INT PRIMARY KEY,
    submitted DATE,
    resolved DATE,
    subjectr TEXT,
    staff_id INT,
    responsible INT,
    FOREIGN KEY (staff_id) REFERENCES staff_member(id),
    FOREIGN KEY (responsible) REFERENCES maintanence_worker(id)
);

CREATE TABLE medicine(
    name VARCHAR(30) PRIMARY KEY,
    amount INT,
    supplier VARCHAR(30)
);

CREATE TABLE surgery(
    id INT PRIMARY KEY,
    date DATE,
    patient_id INT,
    doctor_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

CREATE TABLE meds_for_surgery(
    doctor_id INT,
    med VARCHAR(30),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id),
    FOREIGN KEY (med) REFERENCES medicine(name)
);

CREATE TABLE doctors_report(
    appointment_id INT,
    text TEXT,
    FOREIGN KEY (appointment_id) REFERENCES appointment(id)
);

CREATE TABLE medical_history(
    patient_id INT,
    date DATE,
    record TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);

CREATE TABLE emergency_appointment(
    id INT PRIMARY KEY,
    time TIME,
    date DATE,
    patient_id INT,
    doctor_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

CREATE TABLE staff_meeting(
    date DATE PRIMARY KEY,
    topic VARCHAR(30),
    invited TEXT -- List of ids. Should be separate table, but did it like this, to simplify the DB.
    -- In case it's wrong and you need a separate table - add it.
);

CREATE TABLE food(
    name VARCHAR(30) PRIMARY KEY,
    amount INT,
    supplier VARCHAR(30),
    can_be_allergic BIT -- Boolean
);

CREATE TABLE CCTV_rec(
    date DATE,
    camera_num INT,
    PRIMARY KEY(date, camera_num)
);

CREATE TABLE event(
    id INT PRIMARY KEY,
    title VARCHAR(40)
);

CREATE TABLE display_event( -- In the noticeboard
    person INT,
    event INT,
    FOREIGN KEY (person) REFERENCES person(id),
    FOREIGN KEY (event) REFERENCES event(id)
);

CREATE TABLE notification( -- To be displayed at the noticeboard
    person_id INT,
    topic VARCHAR(40),
    FOREIGN KEY (person_id) REFERENCES person(id)
);

CREATE TABLE invoice( -- To be displayed at the noticeboard
    id INT UNIQUE,
    date DATE,
    amount INT,
    subject TEXT,
    debtor INT,
    FOREIGN KEY (debtor) REFERENCES person(id)
);

CREATE TABLE email(
    date DATE,
    time TIME,
    sent INT,
    recived INT,
    FOREIGN KEY (sent) REFERENCES person(id),
    FOREIGN KEY (recived) REFERENCES person(id)
);

CREATE TABLE request_med(
    date DATE PRIMARY KEY,
    med VARCHAR(30),
    requester INT,
    amount INT,
    FOREIGN KEY (med) REFERENCES medicine(name),
    FOREIGN KEY (requester) REFERENCES staff_member(id)
);

CREATE TABLE request_food(
    date DATE PRIMARY KEY,
    food VARCHAR(30),
    amount INT,
    FOREIGN KEY (food) REFERENCES food(name)
);

CREATE TABLE lab(
    id INT PRIMARY KEY,
    name VARCHAR(30),
    departement_id INT,
    FOREIGN KEY (departement_id) REFERENCES departement(id)
);

CREATE TABLE feedback(
    patient_id INT,
    doctor_id INT,
    text TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient(id), 
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

CREATE TABLE doctors_schedule(
    nurse_id INT,
    doctor_id INT,
    date DATE,
    FOREIGN KEY (nurse_id) REFERENCES nurse(id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(id)
);

CREATE TABLE nurses_schedule(
    nurse_id INT,
    date DATE,
    shift VARCHAR(6), -- 'Day" or 'Night'
    FOREIGN KEY (nurse_id) REFERENCES nurse(id)
);  

CREATE TABLE priests_schedule(
    date DATE,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);






----------------------------------------------------------------