drop database arrzi;
create database arrzi;
use arrzi;

CREATE TABLE `cities` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`city_name` VARCHAR(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE `contractors` (
	`contractor_id` INT NOT NULL AUTO_INCREMENT,
	`email` VARCHAR(255) NOT NULL UNIQUE,
	`dob` VARCHAR(255),
	`aadhar_number` VARCHAR(12),
	`city` INT,
	`registered_date` DATE NOT NULL,
	`phone_number` DECIMAL,
	`full_name` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`contractor_id`,`email`)
);

CREATE TABLE `worker_skills` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`skill_name` VARCHAR(255) NOT NULL UNIQUE,
	PRIMARY KEY (`id`)
);

-- CREATE TABLE `sub_skills` (
-- 	`id` INT NOT NULL AUTO_INCREMENT,
-- 	`skill_id` INT NOT NULL,
-- 	`sub_skill_name` VARCHAR(255) NOT NULL UNIQUE,
-- 	PRIMARY KEY (`id`)
-- );

CREATE TABLE `workers` (
	`worker_id` INT NOT NULL AUTO_INCREMENT,
	`phone_number` DECIMAL NOT NULL UNIQUE,
	`aadhar_number` VARCHAR(12) UNIQUE,
	`dob` VARCHAR(255),
	`city` INT,
	`full_name` VARCHAR(255),
	`start_date` DATE,
	`notification_token` VARCHAR(255),
	`skill` INT,
	`notification_permission` ENUM('True','False'),
	-- `sub_skill` INT,
	PRIMARY KEY (`worker_id`)
);

CREATE TABLE `assignments` (
	`assignment_id` INT NOT NULL AUTO_INCREMENT,
	`contractor_id` INT NOT NULL,
	`create_date` DATE NOT NULL,
	`start_date` DATE NOT NULL,
	`end_date` DATE NOT NULL,
	`worker_needed` INT NOT NULL,
	`wage` INT NOT NULL,
	`skill_needed` INT NOT NULL,
	-- `sub_skill_needed` INT,
	`city` INT NOT NULL,
	`worker_assigned` INT NOT NULL,
	`status` ENUM('active','deleted', 'completed'),
	`description` TEXT,
	`custom_name` VARCHAR(255),
	PRIMARY KEY (`assignment_id`)
);

CREATE TABLE `assignment_status` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`assignment_id` INT NOT NULL,
	`worker_id` INT NOT NULL,
	`status` ENUM('requested','accepted', 'rejected'),
	PRIMARY KEY (`id`)
);

-- CREATE TABLE `rejected_assignments` (
-- 	`id` INT NOT NULL AUTO_INCREMENT,
-- 	`assignment_id` INT NOT NULL,
-- 	`worker_id` INT NOT NULL,
-- 	PRIMARY KEY (`id`)
-- );

-- CREATE TABLE `accepted_assignments` (
-- 	`id` BINARY NOT NULL AUTO_INCREMENT,
-- 	`assignment_id` INT NOT NULL,
-- 	`worker_id` INT NOT NULL,
-- 	PRIMARY KEY (`id`)
-- );

CREATE TABLE `attendance` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`assignment_id` INT NOT NULL,
	`worker_id` INT NOT NULL,
	`attendance` DATE, -- make set datatype
	PRIMARY KEY (`id`)
);

ALTER TABLE `contractors` ADD CONSTRAINT `contractors_fk0` FOREIGN KEY (`city`) REFERENCES `cities`(`id`);

ALTER TABLE `workers` ADD CONSTRAINT `workers_fk0` FOREIGN KEY (`city`) REFERENCES `cities`(`id`);

ALTER TABLE `workers` ADD CONSTRAINT `workers_fk1` FOREIGN KEY (`skill`) REFERENCES `worker_skills`(`id`);

ALTER TABLE `workers` ADD CONSTRAINT `workers_fk2` FOREIGN KEY (`sub_skill`) REFERENCES `sub_skills`(`id`);

ALTER TABLE `assignments` ADD CONSTRAINT `assignments_fk0` FOREIGN KEY (`contractor_id`) REFERENCES `contractors`(`contractor_id`);

ALTER TABLE `assignments` ADD CONSTRAINT `assignments_fk1` FOREIGN KEY (`city`) REFERENCES `cities`(`id`);

ALTER TABLE `assignments` ADD CONSTRAINT `assignments_fk2` FOREIGN KEY (`skill_needed`) REFERENCES `worker_skills`(`id`);

ALTER TABLE `assignments` ADD CONSTRAINT `assignments_fk3` FOREIGN KEY (`sub_skill_needed`) REFERENCES `sub_skills`(`id`);

ALTER TABLE `assignment_status` ADD CONSTRAINT `assignment_status_fk0` FOREIGN KEY (`assignment_id`) REFERENCES `assignments`(`assignment_id`);

ALTER TABLE `assignment_status` ADD CONSTRAINT `assignment_status_fk1` FOREIGN KEY (`worker_id`) REFERENCES `workers`(`worker_id`);

-- ALTER TABLE `rejected_assignments` ADD CONSTRAINT `rejected_assignments_fk0` FOREIGN KEY (`assignment_id`) REFERENCES `assignments`(`assignment_id`);

-- ALTER TABLE `rejected_assignments` ADD CONSTRAINT `rejected_assignments_fk1` FOREIGN KEY (`worker_id`) REFERENCES `workers`(`worker_id`);

-- ALTER TABLE `accepted_assignments` ADD CONSTRAINT `accepted_assignments_fk0` FOREIGN KEY (`assignment_id`) REFERENCES `assignments`(`assignment_id`);

-- ALTER TABLE `accepted_assignments` ADD CONSTRAINT `accepted_assignments_fk1` FOREIGN KEY (`worker_id`) REFERENCES `workers`(`worker_id`);

ALTER TABLE `attendance` ADD CONSTRAINT `attendance_fk0` FOREIGN KEY (`assignment_id`) REFERENCES `assignments`(`assignment_id`);

ALTER TABLE `attendance` ADD CONSTRAINT `attendance_fk1` FOREIGN KEY (`worker_id`) REFERENCES `workers`(`worker_id`);










