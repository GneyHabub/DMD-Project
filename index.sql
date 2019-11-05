-- /Users/gneyhabub/Documents/GitHub/DMD-Project/index.sql

drop table person;
drop table staff_member;

create table person(
    id INT primary key not null,
    full_name VARCHAR(50) not null,
    email VARCHAR(50),
    user_login VARCHAR(30) not null,
    user_password VARCHAR(30) not null,
    sex VARCHAR(1),
    date_of_birth VARCHAR(10),
    age INT,
    permission_level INT not null,
    contact_details VARCHAR(50)
);

create table staff_member(
    id INT,
    position VARCHAR(20),
    salary INT,
    working_hours VARCHAR,
    FOREIGN KEY(id) REFERENCES person(id)
);
