CREATE DATABASE Laptop;

CREATE TABLE `Laptop`.`Dell`(
    `Date` DATE NOT NULL,
    `ID` VARCHAR(25) NOT NULL,
    `ModelName` VARCHAR(50) NOT NULL,
    `Price` SMALLINT unsigned NOT NULL,
    `DateGap` SMALLINT unsigned NOT NULL,
    PRIMARY KEY(`ID`,`Date`)
);

CREATE TABLE `Laptop`.`HP`(
    `Date` DATE NOT NULL,
    `Oid` int NOT NULL,
    `ProductType` VARCHAR(20) NOT NULL,
    `ModleName` VARCHAR(100) NOT NULL,
    `DelieverMSG` VARCHAR(50) NOT NULL,
    `RegularPrice` SMALLINT unsigned NOT NULL,
    `SalePrice` SMALLINT unsigned NOT NULL,
    PRIMARY KEY(`Oid`, `Date`)
)

CREATE DATABASE phone;
CREATE TABLE `phone`.`iPhone`(
    `Country` VARCHAR(2) NOT NULL,
    `TimeStemp` DATE NOT NULL,
    `Product` VARCHAR(20) NOT NULL,
    `Colors` VARCHAR(10) NOT NULL,
    `Size` VARCHAR(5) NOT NULL,
    `Deliver` VARCHAR(30) NOT NULL,
    `Day` SMALLINT unsigned NOT NULL,
    `Celluar` VARCHAR(15),
    PRIMARY KEY(`Country`,`Product`,`Colors`,`Size`,`Celluar`, `TimeStemp`)
)