/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS users (
user_name
phone_number INT(8) NOT NULL,
email VARCHAR(64) PRIMARY KEY CHECK(email LIKE '%_@_%._%' ),
status VARCHAR(64) NOT NULL CHECK(status = 'Buddy' OR status = 'Client' OR status = 'Both'),
display_name VARCHAR(64) NOT NULL,
passwd VARCHAR(10) NOTNULL CHECK((LENGTH(passwd) BETWEEN 8 AND 20) 
								 AND passwd LIKE '(.*[a-z].*)(.*[A-Z].*)(.*\d.*)(.*\W.*)',
gender VARCHAR(64) NOT NULL CHECK(gender = 'Male' OR gender = 'Female' OR gender = 'Prefer not to say'),
birthdate DATE NOT NULL CHECK(DATEDIFF(year,birthdate,GETDATE())>=18),
vaccination_status BINARY(1)
);

CREATE TABLE IF NOT EXISTS buddies (
phone_number INT(8) NOT NULL,
education VARCHAR(256),
interest VARCHAR(256),
height DECIMAL(5,2),
rate_per_hour DECIMAL NOT NULL,
availability VARCHAR(256) NOT NULL,
photo VARCHAR(256) CHECK((photo LIKE '%.jpg') OR (photo LIKE '%.png') OR (photo LIKE '%.jpeg'))
PRIMARY KEY phone_number,
FOREIGN KEY (phone_number) REFERENCES all_users(phone_number) ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE If NOT EXISTS meeting_log (
meeting_id INT PRIMARY KEY UNIQUE,
buddy INT(8) REFERENCES buddy(phone_number) DEFERRABLE,
client INT(8) REFERENCES client(phone_number) DEFERRABLE,
rating_on_buddy INT(1) CHECK(rating BETWEEN 1 AND 5),
rating_on_client INT(1) CHECK(rating BETWEEN 1 AND 5),	
);

