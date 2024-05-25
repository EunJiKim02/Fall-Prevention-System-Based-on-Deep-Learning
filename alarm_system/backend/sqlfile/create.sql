CREATE DATABASE fall default CHARACTER SET UTF8;

use fall;

CREATE TABLE MANAGER(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    email VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL,
    name VARCHAR(256) NOT NULL,
    PRIMARY key (id, email)
) CHARSET=UTF8;

CREATE TABLE PATIENT(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    loc VARCHAR(256) NOT NULL,
    nurse VARCHAR(256),
    significant VARCHAR(512),
    pic_url VARCHAR(256),
    current_status BOOLEAN,
    PRIMARY key (id)
) CHARSET=UTF8;

commit;