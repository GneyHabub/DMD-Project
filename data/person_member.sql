
INSERT INTO person (id,first_name,second_name,email,user_login,user_password,sex,date_of_birth,age,permission_level) VALUES (875,'John','Olson','perrykevin@hotmail.com','john35','GEZZBzBNkR','M','1941-04-28',78,1);
INSERT INTO staff_member (id,employed_since,position,salary,room) VALUES (875,'2016-07-08','Head Doctor',100000,1);
INSERT INTO head_doctor (id,primary_speciality) VALUES (875,'Colon Surgeon');
INSERT INTO person (id,first_name,second_name,email,user_login,user_password,sex,date_of_birth,age,permission_level) VALUES (988,'Jessica','Johnson','iprice@hotmail.com','jamesjones','gsPwBGmzdAnyz','F','1988-09-18',31,1);
INSERT INTO patient (id) VALUES (988);
INSERT INTO person (id,first_name,second_name,email,user_login,user_password,sex,date_of_birth,age,permission_level) VALUES (296,'Barbara','Jennings','elizabeth58@gmail.com','kevin01','ZhmyUrYa','F','1907-12-25',112,1);
INSERT INTO staff_member (id,employed_since,position,salary,room) VALUES (296,'2011-02-10','Cleaning Team Worker',10000,53);
INSERT INTO cleaning_team_worker (id,employment_type) VALUES (296,'Full time');
INSERT INTO person (id,first_name,second_name,email,user_login,user_password,sex,date_of_birth,age,permission_level) VALUES (319,'Linda','Turner','christophermckinney@gmail.com','melissapeterson','QaLPVBDGC','F','1997-04-21',22,1);
INSERT INTO staff_member (id,employed_since,position,salary,room) VALUES (319,'2019-05-03','Professor',35000,35);
INSERT INTO professor (id,reasearch_topic,surgery_participation,departement_id) VALUES (319,'Radiologist',B'0',8);
INSERT INTO person (id,first_name,second_name,email,user_login,user_password,sex,date_of_birth,age,permission_level) VALUES (999,'Julie','Taylor','rlewis@hotmail.com','mossmadison','UuDsrFlaJLifPaF','F','1911-07-08',108,5);
INSERT INTO staff_member (id,employed_since,position,salary,room) VALUES (999,'2015-07-18','Maintanence Worker',15000,57);
INSERT INTO maintanence_worker (id,employment_type,speciality) VALUES (999,'Full time','Electricity');