SELECT user FROM mysql.user;
CREATE DATABASE misha;
USE misha;
GRANT ALL PRIVILEGES ON misha.* TO 'misha_app'@'localhost';
CREATE USER 'misha_app'@'localhost' IDENTIFIED BY 'misha_pass';


CREATE TABLE IF NOT EXISTS clients
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(31) NOT NULL,
    surname varchar(31) NOT NULL,
    fathername varchar(31) NOT NULL,
    passportid varchar(15) NOT NULL,
    country varchar(25) NOT NULL,
    phone_number varchar(15) NOT NULL,
    password varchar(111) NOT NULL
);

CREATE TABLE IF NOT EXISTS cars
(
    id int primary key NOT NULL AUTO_INCREMENT,
    vin varchar(17) NOT NULL,
    number varchar(9) NOT NULL,
    mark varchar(31) NOT NULL,
    model varchar(31) NOT NULL,
    year int NOT NULL,
    fuel enum('бензин', 'дизель', 'гибрид', 'электричество') NOT NULL default 'бензин'
);

CREATE TABLE IF NOT EXISTS car_type
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(21) NOT NULL,
    cost decimal NOT NULL
);

CREATE TABLE IF NOT EXISTS life_type
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(21) NOT NULL,
    cost decimal NOT NULL,
    duration int NOT NULL
);

CREATE TABLE user_car
(
    id int primary key NOT NULL AUTO_INCREMENT,
    idcar int NOT NULL,
    iduser int NOT NULL,
    idtype int NOT NULL,
    timing timestamp default NOW(),
    FOREIGN KEY (idcar) REFERENCES cars (id) ON DELETE CASCADE,
    FOREIGN KEY (iduser) REFERENCES clients (id) ON DELETE CASCADE,
    FOREIGN KEY (idtype) REFERENCES car_type (id) ON DELETE CASCADE
);

CREATE TABLE user_life
(
    id int primary key NOT NULL AUTO_INCREMENT,
    iduser int NOT NULL,
    idtype int NOT NULL,
    timing timestamp default NOW(),
    FOREIGN KEY (iduser) REFERENCES clients (id) ON DELETE CASCADE,
    FOREIGN KEY (idtype) REFERENCES life_type (id) ON DELETE CASCADE
);


INSERT INTO car_type (name, cost)
VALUES ('КАСКО', 85),
       ('Cтандарт', 55),
       ('Про', 125),
       ('Cпортивная', 155);

INSERT INTO life_type (name, cost, duration)
VALUES ('Детский', 45, 12),
       ('Cтандарт', 55, 12),
       ('Путешествия', 55, 2),
       ('Cпортивная', 65, 6);


