-- /Users/gneyhabub/Documents/GitHub/DMD-Project/index.sql


drop table person;
drop table contact_details;
drop table staff_member;
drop table head_doctor;
drop table reseptionist;
drop table maintanence_worker;
drop table cleaning_team_worker;
drop table security_team_member;
drop table hr;
drop table pharmasist;
drop table cook;
drop table priest;
drop table head_nurse;
drop table nurse;
drop table IT_specialist;
drop table proff;
drop table doctor;
drop table doc_education;
drop table patient;
drop table patients_address;
drop table lab_technician;
drop table appointment;
drop table patient_complaint;
drop table IT_complaint;
drop table staff_complaint;

create table person(
    id INT primary key not null unique,
    full_name VARCHAR(50) not null, -- Supposed to ba composite, but SQL doesn't support it, so let it be just a string
    email VARCHAR(50),
    user_login VARCHAR(30) not null default 'login',
    user_password VARCHAR(30) not null default '12345',
    sex VARCHAR(1) not null,
    date_of_birth DATE,
    age INT not null,
    permission_level INT not null default 0
);

create table contact_details(
    id INT,
    foreign key(id) references person(id),
    phone VARCHAR(20),
    telegram VARCHAR(30),
    other VARCHAR(50)
);

create table staff_member(
    id INT unique,
    foreign key(id) references person(id),
    position VARCHAR(20),
    salary INT not null,
    working_hours VARCHAR,
    employed_since DATE not null,
    room VARCHAR(10)
);

create table head_doctor(
    id INT,
    foreign key(id) references person(id),
    primary_speciality VARCHAR(20)
);

create table reseptionist(
    id INT,
    foreign key(id) references person(id),
    spoken_languages VARCHAR(100) default 'English' -- The same as in full name. we either crewate a new table, or just make it string.
);

create table maintanence_worker(
    id INT,
    foreign key(id) references person(id),
    employment_type VARCHAR(9) not null, -- Strictly 'Part time' or 'Full time' only
    speciality VARCHAR(100) -- Composite again
);

create table cleaning_team_worker(
    id INT,
    foreign key(id) references person(id),
    employment_type VARCHAR(9) -- Strictly 'Part time' or 'Full time' only
);

create table security_team_member(
    id INT,
    foreign key(id) references person(id),
    shifts VARCHAR(5) not null, -- 'Night' or 'Day' only
    physical_test_grade VARCHAR(1) -- A, B, C or D
);

create table hr(
    id INT,
    foreign key(id) references person(id),
    selection_responsibility VARCHAR(10)-- Strictly 'Interview' or 'Review' only
);

create table pharmasist(
    id INT,
    foreign key(id) references person(id),
    education_level VARCHAR (15), -- 'Bachelor', 'Magister', 'Postgraduate', 'PhD'
    reasearch BIT not null-- Analogus to Boolean. 1 - True, 0 - False
);

create table cook(
    id INT,
    foreign key(id) references person(id),
    experience INT -- Years
);

create table priest(
    id INT,
    foreign key(id) references person(id),
    religion VARCHAR(15)
);

create table head_nurse(
    id INT,
    foreign key(id) references person(id),
    surgery_assistant BIT not null -- Whether or not he/she sometimes assist in surgeries
);

create table nurse(
    id INT,
    foreign key(id) references person(id),
    surgery_assistant BIT not null, -- Whether or not he/she sometimes assist in surgeries
    preferred_shifts VARCHAR(5), -- 'Night' or 'Day' only
    appointment_assistant BIT not null -- Whether or not he/she sometimes assist during appointments
);

create table IT_specialist(
    id INT,
    foreign key(id) references person(id),
    support_line BIT not null
);

create table proff(
    id INT,
    foreign key(id) references person(id),
    reasearch_topic VARCHAR(50),
    surgery_participation BIT not null
);

create table doctor(
    id INT,
    foreign key(id) references person(id),
    speciality VARCHAR(30),
    emergency_hours BIT not null, -- Has them or not
    experience INT default 0 -- Number of years in the industry
);

create table doc_education(
    id INT,
    foreign key(id) references doctor(id),
    univercity VARCHAR(30),
    graduated DATE,
    degree VARCHAR (10) -- 'Bachelor', 'Magister', 'PhD'
);

create table patient(
    id INT,
    foreign key(id) references person(id),
    registration_date DATE not null default now(),
    allergies VARCHAR(100), -- multivalued
    occupation VARCHAR(50)
);

create table patients_address(
    id INT,
    foreign key(id) references patient(id),
    country VARCHAR(30) default 'Russian Federation',
    district VARCHAR(40) default 'Tatarstan',
    city VARCHAR(20) default 'Innopolis',
    street VARCHAR(30),
    house VARCHAR(8),
    apartement VARCHAR(8)
);

create table lab_technician(
    id INT,
    foreign key(id) references person(id),
    education_level VARCHAR (15) -- 'Bachelor', 'Magister', 'Postgraduate', 'PhD'
);

create table appointment(
    id INT primary key,
    date DATE,
    patient_id INT,
    doctor_id INT,
    foreign key (patient_id) references patient(id),
    foreign key (dictor_id) references doctor(id)
);

create table patient_complaint(
    id INT primary key,
    submitted DATE,
    resolved DATE,
    subjectr VARCHAR(150),
    patient_id INT,
    foreign key (patient_id) references patient(id)
);

create table IT_complaint(
    id INT primary key,
    submitted DATE,
    resolved DATE,
    subjectr VARCHAR(150),
    user_id INT,
    foreign key (user_id) references person(id)
);

create table staff_complaint(
    id INT primary key,
    submitted DATE,
    resolved DATE,
    subjectr VARCHAR(150),
    staff_id INT,
    foreign key (staff_id) references staff_member(id)
);
