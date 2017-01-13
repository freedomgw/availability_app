BEGIN;
CREATE DATABASE availability_db_dev;
COMMIT;

BEGIN;
USE availability_db_dev;

CREATE TABLE user (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  password BLOB NOT NULL,
  UNIQUE (email)
);

CREATE TABLE role (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  description VARCHAR(50) NOT NULL
);

CREATE TABLE user_role (
  user_id INT(6) UNSIGNED NOT NULL,
  role_id INT(6) UNSIGNED NOT NULL,

  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE address (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  user_id INT(6) UNSIGNED NOT NULL,
  street_no INT NOT NULL,
  street_name VARCHAR(50) NOT NULL,
  city VARCHAR(50) NOT NULL,
  province VARCHAR(50) NOT NULL,
  postal_code VARCHAR(50) NOT NULL,
  country VARCHAR(50) NOT NULL,

  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE event (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  customer_id INT(6) UNSIGNED,
  host_id INT(6) UNSIGNED NOT NULL,
  start_date DATETIME NOT NULL,
  end_date DATETIME NOT NULL,

  FOREIGN KEY (customer_id) REFERENCES user(id),
  FOREIGN KEY (host_id) REFERENCES user(id)
);

COMMIT;
