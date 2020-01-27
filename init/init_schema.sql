CREATE DATABASE  IF NOT EXISTS  default_database_/*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE default_database_;
-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: chi_med_baike_lll
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dead_urls_tbl`
--

DROP TABLE IF EXISTS `dead_urls_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `dead_urls_tbl` (
  `url` varchar(200) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `relative` varchar(20) DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `type` varchar(200) DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dead_urls_tbl`
--

LOCK TABLES `dead_urls_tbl` WRITE;
/*!40000 ALTER TABLE `dead_urls_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `dead_urls_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `new_urls_tbl`
--

DROP TABLE IF EXISTS `new_urls_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `new_urls_tbl` (
  `url` varchar(200) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `relative` varchar(20) DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `type` varchar(200) DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `new_urls_tbl`
--

LOCK TABLES `new_urls_tbl` WRITE;
/*!40000 ALTER TABLE `new_urls_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `new_urls_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `old_urls_tbl`
--

DROP TABLE IF EXISTS `old_urls_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `old_urls_tbl` (
  `url` varchar(200) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `relative` varchar(20) DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `type` varchar(200) DEFAULT NULL,
  `file_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `old_urls_tbl`
--

LOCK TABLES `old_urls_tbl` WRITE;
/*!40000 ALTER TABLE `old_urls_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `old_urls_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'chi_med_baike_lll'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-29 10:12:09


grant all privileges on default_database_.* to HunterHan@localhost;
flush privileges;