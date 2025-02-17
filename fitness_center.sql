CREATE DATABASE fitness_center;
USE fitness_center;

CREATE TABLE workout_sessions (
id INT AUTO_INCREMENT PRIMARY KEY,
instructor VARCHAR(35) NOT NULL,
duration TIMESTAMP
);

CREATE TABLE members(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(35) NOT NULL,
email VARCHAR (60) NOT NULL,
start_date DATE,
session_id INT,
FOREIGN KEY (session_id) REFERENCES workout_sessions(id)
);
INSERT INTO members (session_id) 
VALUES(4),
WHERE name ='Arei';


INSERT INTO members (name,email,start_date)
VALUES ('Arei','getFit@gmail.com','2023-01-12'),
('Jess','hotFit@gmail.com','2023-02-14'),
('Rob','musclePower@gmail.com','2019-5-23');

ALTER TABLE workout_sessions
ADD (session_date DATE);

ALTER TABLE workout_sessions
ADD(category VARCHAR(25));

ALTER TABLE workout_sessions
ADD(member_id INT);

ALTER TABLE workout_sessions
ADD (FOREIGN KEY (member_id) REFERENCES members(id));

ALTER TABLE workout_sessions
DROP COLUMN duration;

ALTER TABLE workout_sessions
ADD (duration VARCHAR(15));

INSERT INTO workout_sessions (instructor,duration,session_date,category)
VALUES ('SUZY B','45mins','2024-07-05','ZUMBA'),
('Vicky','50mins','2024-07-03','EXTREME HIPHOP STEP'),
('CKING','45mins','2023-08-09','TOTAL BODY PUMP');
