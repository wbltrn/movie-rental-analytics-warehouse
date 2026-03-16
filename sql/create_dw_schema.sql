DROP DATABASE IF EXISTS movie_rental_dw;
CREATE DATABASE movie_rental_dw;
USE movie_rental_dw;

-- =========================================================
-- Dimension Tables
-- =========================================================

CREATE TABLE dim_customer (
    customer_key INT NOT NULL AUTO_INCREMENT,
    customer_id SMALLINT UNSIGNED NOT NULL,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    email VARCHAR(50),
    active BOOLEAN NOT NULL,
    create_date DATETIME NOT NULL,
    store_id TINYINT UNSIGNED NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_key),
    UNIQUE KEY uq_dim_customer_customer_id (customer_id)
);

CREATE TABLE dim_film (
    film_key INT NOT NULL AUTO_INCREMENT,
    film_id SMALLINT UNSIGNED NOT NULL,
    title VARCHAR(128) NOT NULL,
    release_year YEAR,
    rental_duration TINYINT UNSIGNED NOT NULL,
    rental_rate DECIMAL(4,2) NOT NULL,
    length SMALLINT UNSIGNED,
    replacement_cost DECIMAL(5,2) NOT NULL,
    rating VARCHAR(10),
    PRIMARY KEY (film_key),
    UNIQUE KEY uq_dim_film_film_id (film_id)
);

CREATE TABLE dim_store (
    store_key INT NOT NULL AUTO_INCREMENT,
    store_id TINYINT UNSIGNED NOT NULL,
    manager_staff_id TINYINT UNSIGNED NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    PRIMARY KEY (store_key),
    UNIQUE KEY uq_dim_store_store_id (store_id)
);

CREATE TABLE dim_staff (
    staff_key INT NOT NULL AUTO_INCREMENT,
    staff_id TINYINT UNSIGNED NOT NULL,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    email VARCHAR(50),
    active BOOLEAN NOT NULL,
    username VARCHAR(16) NOT NULL,
    store_id TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (staff_key),
    UNIQUE KEY uq_dim_staff_staff_id (staff_id)
);
