BEGIN;

USE availability_db_dev;

INSERT INTO role (created_at, updated_at, description) VALUES (NOW(), NOW(), 'babysitter');

COMMIT;