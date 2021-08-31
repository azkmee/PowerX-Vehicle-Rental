SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `Transactions`;
DROP TABLE IF EXISTS `Users`;
DROP TABLE IF EXISTS `Vehicles`;
DROP TABLE IF EXISTS `Demerits`;
DROP TABLE IF EXISTS `Vouchers`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `Transactions` (
    `tid` INTEGER NOT NULL,
    `vid` INTEGER NOT NULL,
    `cid` INTEGER NOT NULL,
    `book_duration` FLOAT NOT NULL,
    `start_time` DATETIME NOT NULL,
    `end_time` DATETIME,
    `start_odometer` FLOAT NOT NULL,
    `end_odometer` FLOAT,
    `amount` DECIMAL(2) NOT NULL,
    `addditional_fee` DECIMAL(2),
    `isPaid` BOOLEAN NOT NULL,
    PRIMARY KEY (`tid`)
);

CREATE TABLE `Users` (
    `uid` INTEGER NOT NULL,
    `type` VARCHAR(10) NOT NULL,
    `full_name` VARCHAR(200) NOT NULL,
    `dob` DATE NOT NULL,
    `email` VARCHAR(150) NOT NULL,
    `mobile` VARCHAR(20) NOT NULL,
    `address` VARCHAR(500) NOT NULL,
    `wallet` DECIMAL(2) NOT NULL,
    `isActive` BOOLEAN NOT NULL,
    PRIMARY KEY (`uid`)
);

CREATE TABLE `Vehicles` (
    `vid` INTEGER NOT NULL,
    `type` VARCHAR(15) NOT NULL,
    `brand` VARCHAR(35) NOT NULL,
    `model` VARCHAR(100) NOT NULL,
    `number_plate` VARCHAR(15) NOT NULL,
    `purchase_date` DATE NOT NULL,
    `odometer` FLOAT NOT NULL,
    `health` FLOAT NOT NULL,
    `unit_price` DECIMAL(2) NOT NULL,
    `isAvailable` BOOLEAN NOT NULL,
    PRIMARY KEY (`vid`),
    UNIQUE (`number_plate`)
);

CREATE TABLE `Demerits` (
    `did` INTEGER NOT NULL,
    `tid` INTEGER NOT NULL,
    `cid` INTEGER NOT NULL,
    `demerit_date` DATE NOT NULL,
    `description` VARCHAR(2000) NOT NULL,
    `points` INTEGER NOT NULL,
    `isActive` BOOLEAN NOT NULL,
    PRIMARY KEY (`did`)
);

CREATE TABLE `Vouchers` (
    `vou_id` INTEGER NOT NULL,
    `cid` INTEGER NOT NULL,
    `tid` INTEGER,
    `discount` DECIMAL(2) NOT NULL,
    `issue_date` DATE NOT NULL,
    `exp_date` DATE NOT NULL,
    PRIMARY KEY (`vou_id`)
);
