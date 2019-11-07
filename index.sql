-- /Users/gneyhabub/Documents/GitHub/DMD-Project/index.sql

DROP TABLE surgery;
DROP TABLE meds_for_surgery;
DROP TABLE doctors_report;
DROP TABLE medical_history;
DROP TABLE staff_meeting;
DROP TABLE CCTV_rec;
DROP TABLE event;
DROP TABLE notification;
DROP TABLE invoice;
DROP TABLE email;
DROP TABLE request_med;
DROP TABLE request_food;
DROP TABLE depaertement;
DROP TABLE lab;
DROP TABLE food;
DROP TABLE medicine;
DROP TABLE contact_details;
DROP TABLE head_doctor;
DROP TABLE reseptionist;
DROP TABLE maintanence_worker;
DROP TABLE cleaning_team_worker;
DROP TABLE security_team_member;
DROP TABLE hr;
DROP TABLE pharmasist;
DROP TABLE cook;
DROP TABLE priest;
DROP TABLE head_nurse;
DROP TABLE nurse;
DROP TABLE IT_specialist;
DROP TABLE proff;
DROP TABLE doc_education;
DROP TABLE patients_address;
DROP TABLE lab_technician;
DROP TABLE appointment;
DROP TABLE patient_complaint;
DROP TABLE IT_complaint;
DROP TABLE staff_complaint;
DROP TABLE staff_member;
DROP TABLE patient;
DROP TABLE doctor;
DROP TABLE person;

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

CREATE TABLE head_doctor(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    primary_speciality VARCHAR(20)
);

CREATE TABLE reseptionist(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    spoken_languages VARCHAR(100) default 'English' -- The same as in full name. we either crewate a new table, or just make it string.
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
    appointment_assistant BIT NOT NULL -- Whether or not he/she sometimes assist during appointments
);

CREATE TABLE IT_specialist(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    support_line BIT NOT NULL
);

CREATE TABLE proff(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    reasearch_topic VARCHAR(50),
    surgery_participation BIT NOT NULL
);

CREATE TABLE doctor(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    speciality VARCHAR(30),
    emergency_hours BIT NOT NULL, -- Has them or not
    experience INT default 0 -- Number of years in the industry
);

CREATE TABLE doc_education(
    id INT,
    FOREIGN KEY(id) REFERENCES doctor(id),
    univercity VARCHAR(30),
    graduated DATE,
    degree VARCHAR (10) -- 'Bachelor', 'Magister', 'PhD'
);

CREATE TABLE patient(
    id INT UNIQUE,
    FOREIGN KEY(id) REFERENCES person(id),
    registration_date DATE NOT NULL default now(),
    allergies VARCHAR(100), -- multivalued
    occupation VARCHAR(50)
);

CREATE TABLE patients_address(
    id INT,
    FOREIGN KEY(id) REFERENCES patient(id),
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
    education_level VARCHAR (15) -- 'Bachelor', 'Magister', 'Postgraduate', 'PhD'
);

CREATE TABLE appointment(
    id INT PRIMARY KEY,
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
    subjectr VARCHAR(150),
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);

CREATE TABLE IT_complaint(
    id INT PRIMARY KEY,
    submitted DATE,
    resolved DATE,
    subjectr VARCHAR(150),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES person(id)
);

CREATE TABLE staff_complaint(
    id INT PRIMARY KEY,
    submitted DATE,
    resolved DATE,
    subjectr VARCHAR(150),
    staff_id INT,
    FOREIGN KEY (staff_id) REFERENCES staff_member(id)
);

--------------------------------------------------------------------

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
    appointment INT,
    text VARCHAR(150),
    FOREIGN KEY (appointment) REFERENCES appointment(id)
);

CREATE TABLE medical_history(
    patient INT,
    date DATE,
    record VARCHAR(200),
    FOREIGN KEY (patient) REFERENCES patient(id)
);

-- CREATE TABLE emergency_appointment(

-- );

CREATE TABLE staff_meeting(
    date DATE PRIMARY KEY,
    topic VARCHAR(30),
    invited VARCHAR(150) -- List of ids. Should be separate table, but did it like this, to simplify the DB.
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

CREATE TABLE event( -- To be displayed at the noticeboard
    person INT,
    title VARCHAR(40),
    FOREIGN KEY (person) REFERENCES person(id)
);

CREATE TABLE notification( -- To be displayed at the noticeboard
    person INT,
    topic VARCHAR(40),
    FOREIGN KEY (person) REFERENCES person(id)
);

CREATE TABLE invoice( -- To be displayed at the noticeboard
    id INT UNIQUE,
    date DATE,
    amount INT,
    subject VARCHAR(50),
    debtor INT,
    FOREIGN KEY (debtor) REFERENCES person(id)
);

CREATE TABLE email(
    date DATE,
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

CREATE TABLE depaertement(
    id INT PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE lab(
    id INT PRIMARY KEY,
    name VARCHAR(30)
);