-- Prepares a MySQL server for AirBnB_clone_v2
-- Creates database: hbnb_dev_db
-- Creates new user: hbnb_dev (in localhost)
-- Password of hbnb_dev should be set to: hbnb_dev_pwd
-- hbnb_dev should have all privileges on the database hbnb_dev_db (and only this database)
-- hbnb_dev should have SELECT privilege on the database performance_schema (and only this database)

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

CREATE USER IF NOT EXISTS hbnb_dev@localhost
IDENTIFIED BY 'hbnb_dev_pwd';

GRANT ALL PRIVILEGES
ON hbnb_dev_db.*
TO hbnb_dev@localhost;

GRANT SELECT
ON performance_schema.*
TO hbnb_dev@localhost;