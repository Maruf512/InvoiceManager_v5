-- Active: 1730477691279@@127.0.0.1@3306@nft_management


CREATE DATABASE nft_management


CREATE TABLE catagory(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO catagory(name) VALUES ('Shawl')

INSERT INTO catagory(name) VALUES ('Shawl')

SELECT * FROM catagory

DELETE FROM `catagory` WHERE `id` IN (1,2)




CREATE TABLE products(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    rate INT NOT NULL,
    catagory_id BIGINT UNSIGNED NOT NULL,
    Foreign Key (`catagory_id`) REFERENCES catagory (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO products(name, rate, catagory_id) VALUES ("Flor Mate", 60, 3)

SELECT * FROM products



CREATE TABLE employee(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    nid_no VARCHAR(50) NOT NULL,
    mobile VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO employee(name, address, nid_no, mobile) VALUES ("Lovely", "Garashin", "88888888", "01799999999")

SELECT * FROM employee


-- Production id == roll id (from nowon there willbe no name on the roll, it will only contain YDS and Product id)
CREATE TABLE production(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    products_id BIGINT UNSIGNED NOT NULL,
    employee_id BIGINT UNSIGNED NOT NULL,
    quantity FLOAT NOT NULL,
    rate FLOAT NOT NULL,
    Foreign Key (`products_id`) REFERENCES products (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`employee_id`) REFERENCES employee (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO production(products_id, employee_id, quantity, rate) VALUES (1, 2, 29, 30)

SELECT * FROM production WHERE employee_id=1


CREATE TABLE inventory(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    employee_id BIGINT UNSIGNED NOT NULL,
    products_id BIGINT UNSIGNED NOT NULL,
    production_id BIGINT UNSIGNED NOT NULL,
    current_status VARCHAR(50) DEFAULT 'IN-STOCK' NOT NULL,                     -- Check if it is sold or not if it is sold then change it to SOLD
    Foreign Key (`employee_id`) REFERENCES employee (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`products_id`) REFERENCES products (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`production_id`) REFERENCES production (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO inventory(employee_id, products_id, production_id, current_status) VALUES(1, 1, 2, 'SOLD')


SELECT * FROM inventory



CREATE TABLE employee_bill(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    employee_id BIGINT UNSIGNED NOT NULL,
    production_id BIGINT UNSIGNED NOT NULL,
    total_amount INT NOT NULL,
    current_status VARCHAR(50) DEFAULT 'NOT-PAID' NOT NULL,
    Foreign Key (`employee_id`) REFERENCES employee (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`production_id`) REFERENCES production (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO employee_bill(employee_id, production_id, total_amount) VALUES (1,1,4620)

SELECT * FROM employee_bill WHERE employee_id=1



CREATE TABLE customer(
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL,
    company_name VARCHAR(100) DEFAULT 'NONE' NOT NULL,
    address VARCHAR(100) NOT NULL,
    mobile VARCHAR(50) NOT NULL,
    email VARCHAR(50) DEFAULT 'NONE' NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO customer(name, address, mobile) VALUES('DoggyMan', 'Shokhipur', '01799999999')

SELECT * FROM customer


-- SELECT * FROM inventory WHERE current_status='IN-STOCK' AND employee_id=1 (run this command for one employee)
CREATE TABLE challan(
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT UNSIGNED NOT NULL,
    products_id BIGINT UNSIGNED NOT NULL,
    employee_id BIGINT UNSIGNED NOT NULL,
    production_id BIGINT UNSIGNED NOT NULL,
    current_status VARCHAR(50) DEFAULT 'NOT-PAID' NOT NULL,
    Foreign Key (`products_id`) REFERENCES products (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`customer_id`) REFERENCES customer (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`employee_id`) REFERENCES employee (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`production_id`) REFERENCES production (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

INSERT INTO challan(id, customer_id, products_id, employee_id, production_id) VALUES(1, 1, 1, 1, 2)

SELECT * FROM challan

CREATE TABLE cash_memo(
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    products_id BIGINT UNSIGNED NOT NULL,
    customer_id BIGINT UNSIGNED NOT NULL,
    challan_id BIGINT UNSIGNED NOT NULL,
    total_yds BIGINT NOT NULL,
    total_amount BIGINT NOT NULL,
    Foreign Key (`products_id`) REFERENCES products (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`customer_id`) REFERENCES customer (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    Foreign Key (`challan_id`) REFERENCES challan (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
)


