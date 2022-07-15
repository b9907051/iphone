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

CREATE TABLE `Laptop`.`Bestbuy`(
    `lowprice_average` float(24) NOT NULL,
    `highprice_average` float(24) NOT NULL,
    `soldout_percent` float(24) NOT NULL,
    `onsale_percent` float(24) NOT NULL,
    `total_amount` SMALLINT unsigned NOT NULL,
    `ordeble_amount` SMALLINT unsigned NOT NULL,
    `soldout_amount` SMALLINT unsigned NOT NULL,
    `onsale_amount` SMALLINT unsigned NOT NULL,
    `non_onsale_amount` SMALLINT unsigned NOT NULL,
    `onsale_dollar_percent` float(24) NOT NULL,
    `timestamp` DATE NOT NULL,
    PRIMARY KEY(`timestamp`)
)

CREATE DATABASE Phone;
CREATE TABLE `Phone`.`iPhone`(
    `Country` VARCHAR(2) NOT NULL,
    `TimeStemp` DATE NOT NULL,
    `Product` VARCHAR(20) NOT NULL,
    `Colors` VARCHAR(10) NOT NULL,
    `Size` VARCHAR(5) NOT NULL,
    `Deliver` VARCHAR(50) NOT NULL,
    `Day` SMALLINT unsigned NOT NULL,
    `Celluar` VARCHAR(15),
    PRIMARY KEY(`Country`,`Product`,`Colors`,`Size`,`Celluar`, `TimeStemp`,`Day`,`Deliver`)
)

CREATE DATABASE Sports;
CREATE TABLE `Sports`.`Nike`(
    `timestamp` DATE NOT NULL,
    `discount_item_ratio_cloth` float(24) NOT NULL,
    `discount_money_cloth` float(24) NOT NULL,
    `total_num_cloth` SMALLINT unsigned NOT NULL,
    `soldout_num_cloth` SMALLINT unsigned NOT NULL,
    `instock_num_cloth` SMALLINT unsigned NOT NULL,
    `discount_num_cloth` SMALLINT unsigned NOT NULL,
    `discount_item_ratio_shoes` float(24) NOT NULL,
    `discount_money_shoes` float(24) NOT NULL,
    `total_num_shoes` SMALLINT unsigned NOT NULL,
    `soldout_num_shoes` SMALLINT unsigned NOT NULL,
    `instock_num_shoes` SMALLINT unsigned NOT NULL,
    `discount_num_shoes` SMALLINT unsigned NOT NULL,
    PRIMARY KEY(`timestamp`)
)