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

-- Date dimension is required by the rubric.
-- Your professor said the MySQL code for dim_date is already provided separately.
-- So dim_date should be created in sql/create_dim_date.sql

-- =========================================================
-- Fact Table
-- Grain: one row per payment associated with a rental
-- =========================================================

CREATE TABLE fact_rental_payment (
    fact_rental_payment_key BIGINT NOT NULL AUTO_INCREMENT,
    payment_id SMALLINT UNSIGNED NOT NULL,
    rental_id INT,
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    film_key INT NOT NULL,
    store_key INT NOT NULL,
    staff_key INT NOT NULL,
    payment_amount DECIMAL(5,2) NOT NULL,
    rental_days INT,
    days_late INT,
    is_late BOOLEAN NOT NULL,
    PRIMARY KEY (fact_rental_payment_key),
    UNIQUE KEY uq_fact_payment_id (payment_id),
    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    CONSTRAINT fk_fact_customer
        FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    CONSTRAINT fk_fact_film
        FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    CONSTRAINT fk_fact_store
        FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    CONSTRAINT fk_fact_staff
        FOREIGN KEY (staff_key) REFERENCES dim_staff(staff_key)
);
