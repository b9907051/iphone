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
    `ProdutType` VARCHAR(20) NOT NULL,
    `ModleName` VARCHAR(100) NOT NULL,
    `DelieverMSG` VARCHAR(50) NOT NULL,
    `RegularPrice` SMALLINT unsigned NOT NULL,
    `SalePrice` SMALLINT unsigned NOT NULL,
    PRIMARY KEY(`Oid`, `Date`)
)
