USE movie_rental_dw;

DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_key INT NOT NULL,
    full_date DATE NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_of_month INT NOT NULL,
    day_of_year INT NOT NULL,
    week_of_year INT NOT NULL,
    month_num INT NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    quarter_num INT NOT NULL,
    year_num INT NOT NULL,
    weekend_flag BOOLEAN NOT NULL,
    PRIMARY KEY (date_key),
    UNIQUE KEY uq_dim_date_full_date (full_date)
);

DROP PROCEDURE IF EXISTS populate_dim_date;

DELIMITER $$

CREATE PROCEDURE populate_dim_date(IN start_date DATE, IN end_date DATE)
BEGIN
    DECLARE current_date DATE;

    SET current_date = start_date;

    WHILE current_date <= end_date DO
        INSERT INTO dim_date (
            date_key,
            full_date,
            day_of_week,
            day_name,
            day_of_month,
            day_of_year,
            week_of_year,
            month_num,
            month_name,
            quarter_num,
            year_num,
            weekend_flag
        )
        VALUES (
            CAST(DATE_FORMAT(current_date, '%Y%m%d') AS UNSIGNED),
            current_date,
            DAYOFWEEK(current_date),
            DAYNAME(current_date),
            DAYOFMONTH(current_date),
            DAYOFYEAR(current_date),
            WEEKOFYEAR(current_date),
            MONTH(current_date),
            MONTHNAME(current_date),
            QUARTER(current_date),
            YEAR(current_date),
            CASE
                WHEN DAYOFWEEK(current_date) IN (1, 7) THEN TRUE
                ELSE FALSE
            END
        );

        SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
    END WHILE;
END$$

DELIMITER ;

CALL populate_dim_date('2004-01-01', '2007-12-31');
