-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema proyecto_ideas_brillantes
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema proyecto_ideas_brillantes
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `proyecto_ideas_brillantes` DEFAULT CHARACTER SET utf8 ;
USE `proyecto_ideas_brillantes` ;

-- -----------------------------------------------------
-- Table `proyecto_ideas_brillantes`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_ideas_brillantes`.`users` ;

CREATE TABLE IF NOT EXISTS `proyecto_ideas_brillantes`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `alias` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(500) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_ideas_brillantes`.`posts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_ideas_brillantes`.`posts` ;

CREATE TABLE IF NOT EXISTS `proyecto_ideas_brillantes`.`posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_posts_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `proyecto_ideas_brillantes`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_ideas_brillantes`.`likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_ideas_brillantes`.`likes` ;

CREATE TABLE IF NOT EXISTS `proyecto_ideas_brillantes`.`likes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `post_id` INT NOT NULL,
  `likes` TINYINT NOT NULL DEFAULT 0,
  `iduser_liked` TINYINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_posts_posts1_idx` (`post_id` ASC) VISIBLE,
  INDEX `fk_users_has_posts_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_posts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `proyecto_ideas_brillantes`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_posts_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `proyecto_ideas_brillantes`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
