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
