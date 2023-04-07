-- MySQL dump 10.13  Distrib 8.0.32, for macos11.7 (x86_64)
--
-- Host: localhost    Database: RideShare
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `driver` (
  `driverID` int NOT NULL,
  `fullName` varchar(40) DEFAULT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `licensePlate` varchar(7) DEFAULT NULL,
  `driverMode` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`driverID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES (2,'Bob Treetrunk',5.0,'7GHF890',0),(4,'Mike Sherm',4.5,'6ABC123',1),(8,'Poot Lovato',5.0,'8YYY567',1),(10,'Jay Park',5.0,'5OMG333',0),(11,'Don Toliver',4.0,'8NMT901',1),(13,'Kai Wachi',4.0,'5BUT000',1),(14,'Blue Carrot',3.5,'7ILH980',1);
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rider`
--

DROP TABLE IF EXISTS `rider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rider` (
  `riderID` int NOT NULL,
  `fullName` varchar(40) DEFAULT NULL,
  `creationDate` date DEFAULT NULL,
  PRIMARY KEY (`riderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rider`
--

LOCK TABLES `rider` WRITE;
/*!40000 ALTER TABLE `rider` DISABLE KEYS */;
INSERT INTO `rider` VALUES (1,'Bob Wazowski','2023-04-06'),(3,'Tommy White','2023-04-06'),(5,'Sandy Cheeks','2023-04-06'),(6,'Selena Gomez','2023-04-06'),(7,'Irene Puckett','2023-04-06'),(9,'Sullivan King','2023-04-06'),(12,'Ben Nicky','2023-04-06');
/*!40000 ALTER TABLE `rider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rides`
--

DROP TABLE IF EXISTS `rides`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rides` (
  `rideID` int NOT NULL,
  `pickupLocation` varchar(40) DEFAULT NULL,
  `dropoffLocation` varchar(40) DEFAULT NULL,
  `dateAndTime` datetime DEFAULT NULL,
  `riderID` int DEFAULT NULL,
  `driverID` int DEFAULT NULL,
  PRIMARY KEY (`rideID`),
  KEY `riderID` (`riderID`),
  KEY `driverID` (`driverID`),
  CONSTRAINT `rides_ibfk_1` FOREIGN KEY (`riderID`) REFERENCES `rider` (`riderID`),
  CONSTRAINT `rides_ibfk_2` FOREIGN KEY (`driverID`) REFERENCES `driver` (`driverID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rides`
--

LOCK TABLES `rides` WRITE;
/*!40000 ALTER TABLE `rides` DISABLE KEYS */;
INSERT INTO `rides` VALUES (1,'SNA','Chapman','2023-04-06 21:05:29',6,4),(4,'Orange','Disneyland','2023-04-06 21:09:52',12,4),(5,'Seaside Donuts','Huntington Beach','2023-04-06 21:14:19',12,4),(6,'Chinatown','Koreatown','2023-04-06 21:23:38',12,14),(7,'Blue Bowll','Jamba Juice','2023-04-06 21:25:11',6,4),(8,'Irvine','UCI','2023-04-06 21:25:58',7,8),(9,'Diamond Jamboree','LA Fitness','2023-04-06 21:27:21',1,14),(10,'Universal Studio\'s','Mom\'s house','2023-04-06 21:27:47',3,11),(11,'Gram\'s','Baekjong','2023-04-06 21:28:28',3,13);
/*!40000 ALTER TABLE `rides` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-06 21:32:22
