CREATE DATABASE plants 
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

USE plants;

CREATE TABLE DataPoint (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name CHAR(140) NOT NULL,
	time TIMESTAMP NOT NULL,
	value DOUBLE NOT NULL,
	INDEX(name),
	INDEX USING BTREE (time)
) ENGINE=InnoDB;

CREATE TABLE Cal (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name CHAR(140) NOT NULL,
	value DOUBLE NOT NULL,
	INDEX(name)
) ENGINE=InnoDB;


