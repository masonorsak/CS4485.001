-- MySQL Script generated by MySQL Workbench
-- Thu Apr  1 21:02:14 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema seniordesign
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema seniordesign
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `seniordesign` DEFAULT CHARACTER SET utf8 ;
USE `seniordesign` ;

-- -----------------------------------------------------
-- Table `seniordesign`.`House`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`House` (
  `HouseID` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`HouseID`),
  UNIQUE INDEX `HouseID_UNIQUE` (`HouseID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seniordesign`.`Weather`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`Weather` (
  `WeatherID` INT NOT NULL AUTO_INCREMENT,
  `House_HouseID` INT NOT NULL,
  `apiKey` VARCHAR(32) NULL,
  PRIMARY KEY (`WeatherID`),
  UNIQUE INDEX `WeatherID_UNIQUE` (`WeatherID` ASC) VISIBLE,
  INDEX `fk_Weather_House1_idx` (`House_HouseID` ASC) VISIBLE,
  CONSTRAINT `fk_Weather_House1`
    FOREIGN KEY (`House_HouseID`)
    REFERENCES `seniordesign`.`House` (`HouseID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seniordesign`.`CityData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`CityData` (
  `CityID` INT NOT NULL AUTO_INCREMENT,
  `Weather_WeatherID` INT NOT NULL,
  `zip` INT NULL,
  `lat` FLOAT NULL,
  `long` FLOAT NULL,
  PRIMARY KEY (`CityID`),
  UNIQUE INDEX `CityID_UNIQUE` (`CityID` ASC) VISIBLE,
  INDEX `fk_CityData_Weather1_idx` (`Weather_WeatherID` ASC) VISIBLE,
  CONSTRAINT `fk_CityData_Weather1`
    FOREIGN KEY (`Weather_WeatherID`)
    REFERENCES `seniordesign`.`Weather` (`WeatherID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seniordesign`.`WeatherData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`WeatherData` (
  `WeatherID` INT NOT NULL AUTO_INCREMENT,
  `CityData_CityID` INT NOT NULL,
  `time` INT NULL,
  `temp` FLOAT NULL,
  `humidity` FLOAT NULL,
  `pressure` FLOAT NULL,
  `windSpeed` FLOAT NULL,
  `dewPoint` FLOAT NULL,
  PRIMARY KEY (`WeatherID`),
  UNIQUE INDEX `WeatherID_UNIQUE` (`WeatherID` ASC) VISIBLE,
  INDEX `fk_WeatherData_CityData1_idx` (`CityData_CityID` ASC) VISIBLE,
  CONSTRAINT `fk_WeatherData_CityData1`
    FOREIGN KEY (`CityData_CityID`)
    REFERENCES `seniordesign`.`CityData` (`CityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seniordesign`.`Device`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`Device` (
  `DeviceID` INT NOT NULL AUTO_INCREMENT,
  `House_HouseID` INT NOT NULL,
  `DeviceType` INT NOT NULL,
  PRIMARY KEY (`DeviceID`),
  INDEX `fk_Device_House_idx` (`House_HouseID` ASC) VISIBLE,
  UNIQUE INDEX `DeviceID_UNIQUE` (`DeviceID` ASC) VISIBLE,
  CONSTRAINT `fk_Device_House`
    FOREIGN KEY (`House_HouseID`)
    REFERENCES `seniordesign`.`House` (`HouseID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seniordesign`.`DeviceData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`DeviceData` (
  `DeviceDataID` INT NOT NULL AUTO_INCREMENT,
  `Device_DeviceID` INT NOT NULL,
  `time` INT NULL,
  `energyUse` FLOAT NULL,
  `anomaly` TINYINT NULL,
  PRIMARY KEY (`DeviceDataID`),
  UNIQUE INDEX `DeviceID_UNIQUE` (`DeviceDataID` ASC) VISIBLE,
  INDEX `fk_DeviceData_Device1_idx` (`Device_DeviceID` ASC) VISIBLE,
  CONSTRAINT `fk_DeviceData_Device1`
    FOREIGN KEY (`Device_DeviceID`)
    REFERENCES `seniordesign`.`Device` (`DeviceID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seniordesign`.`DeviceAvg`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`DeviceAvg` (
  `AvgID` INT NOT NULL AUTO_INCREMENT,
  `Device_DeviceID` INT NOT NULL,
  `time` INT NULL,
  `average` FLOAT NULL,
  INDEX `fk_DeviceAvg_Device1_idx` (`Device_DeviceID` ASC) VISIBLE,
  PRIMARY KEY (`AvgID`),
  UNIQUE INDEX `AvgID_UNIQUE` (`AvgID` ASC) VISIBLE,
  CONSTRAINT `fk_DeviceAvg_Device1`
    FOREIGN KEY (`Device_DeviceID`)
    REFERENCES `seniordesign`.`Device` (`DeviceID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seniordesign`.`WeatherAvg`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seniordesign`.`WeatherAvg` (
  `AvgID` INT NOT NULL AUTO_INCREMENT,
  `CityData_CityID` INT NOT NULL,
  `time` INT NULL,
  `tempAvg` FLOAT NULL,
  `humidityAvg` FLOAT NULL,
  `pressureAvg` FLOAT NULL,
  `windSpeedAvg` FLOAT NULL,
  `dewPointAvg` FLOAT NULL,
  PRIMARY KEY (`AvgID`),
  UNIQUE INDEX `AvgID_UNIQUE` (`AvgID` ASC) VISIBLE,
  INDEX `fk_DeviceAvg_copy1_CityData1_idx` (`CityData_CityID` ASC) VISIBLE,
  CONSTRAINT `fk_DeviceAvg_copy1_CityData1`
    FOREIGN KEY (`CityData_CityID`)
    REFERENCES `seniordesign`.`CityData` (`CityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
