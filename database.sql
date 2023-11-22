-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: rozpoznawanieraspsow
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `inception_matrix`
--

DROP TABLE IF EXISTS `inception_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inception_matrix` (
  `id` int NOT NULL AUTO_INCREMENT,
  `predicted_breed` varchar(50) NOT NULL,
  `actual_breed` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inception_matrix`
--

LOCK TABLES `inception_matrix` WRITE;
/*!40000 ALTER TABLE `inception_matrix` DISABLE KEYS */;
INSERT INTO `inception_matrix` VALUES (1,'golden_retriever','golden_retriever'),(2,'german_shepherd','german_shepherd'),(3,'german_shepherd','german_shepherd'),(4,'golden_retriever','golden_retriever'),(5,'golden_retriever','golden_retriever'),(6,'german_shepherd','affenpinscher'),(7,'german_shepherd','affenpinscher'),(8,'german_shepherd','afghan_hound'),(9,'german_shepherd','brak psa na zdjęciu'),(10,'standard_schnauzer','standard_schnauzer');
/*!40000 ALTER TABLE `inception_matrix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `own_inception_matrix`
--

DROP TABLE IF EXISTS `own_inception_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `own_inception_matrix` (
  `id` int NOT NULL AUTO_INCREMENT,
  `predicted_breed` varchar(50) NOT NULL,
  `actual_breed` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `own_inception_matrix`
--

LOCK TABLES `own_inception_matrix` WRITE;
/*!40000 ALTER TABLE `own_inception_matrix` DISABLE KEYS */;
INSERT INTO `own_inception_matrix` VALUES (1,'labrador_retriever','labrador_retriever'),(2,'miniature_schnauzer','miniature_schnauzer');
/*!40000 ALTER TABLE `own_inception_matrix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `own_yolo_matrix`
--

DROP TABLE IF EXISTS `own_yolo_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `own_yolo_matrix` (
  `id` int NOT NULL AUTO_INCREMENT,
  `predicted_breed` varchar(50) NOT NULL,
  `actual_breed` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `own_yolo_matrix`
--

LOCK TABLES `own_yolo_matrix` WRITE;
/*!40000 ALTER TABLE `own_yolo_matrix` DISABLE KEYS */;
INSERT INTO `own_yolo_matrix` VALUES (1,'great_pyrenees','great_pyrenees'),(2,'german_shepherd','german_shepherd');
/*!40000 ALTER TABLE `own_yolo_matrix` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_matrix`
--

DROP TABLE IF EXISTS `test_matrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_matrix` (
  `id` int NOT NULL AUTO_INCREMENT,
  `predicted_breed` varchar(45) DEFAULT NULL,
  `actual_breed` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_matrix`
--

LOCK TABLES `test_matrix` WRITE;
/*!40000 ALTER TABLE `test_matrix` DISABLE KEYS */;
INSERT INTO `test_matrix` VALUES (1,'labrador','labrador'),(2,'labrador','labrador'),(3,'labrador','labrador'),(4,'labrador','labrador'),(5,'labrador','labrador'),(6,'labrador','labrador'),(7,'labrador','labrador'),(8,'labrador','labrador'),(9,'labrador','labrador'),(10,'labrador','labrador'),(11,'golden_retriever','labrador'),(12,'golden_retriever','labrador'),(13,'golden_retriever','labrador'),(14,'golden_retriever','labrador'),(15,'golden_retriever','labrador'),(16,'golden_retriever','labrador'),(17,'golden_retriever','labrador'),(18,'golden_retriever','labrador'),(19,'golden_retriever','labrador'),(20,'golden_retriever','labrador'),(21,'golden_retriever','labrador'),(22,'golden_retriever','labrador'),(23,'golden_retriever','labrador'),(24,'golden_retriever','labrador'),(25,'golden_retriever','labrador'),(26,'golden_retriever','labrador'),(27,'golden_retriever','labrador'),(28,'golden_retriever','labrador'),(29,'golden_retriever','labrador'),(30,'golden_retriever','labrador'),(31,'german_shepherd','german_shepherd'),(32,'german_shepherd','german_shepherd'),(33,'german_shepherd','german_shepherd'),(34,'german_shepherd','german_shepherd'),(35,'german_shepherd','german_shepherd'),(36,'german_shepherd','german_shepherd'),(37,'german_shepherd','german_shepherd'),(38,'german_shepherd','german_shepherd'),(39,'german_shepherd','german_shepherd'),(40,'german_shepherd','german_shepherd'),(41,'german_shepherd','german_shepherd'),(42,'german_shepherd','german_shepherd'),(43,'german_shepherd','german_shepherd'),(44,'german_shepherd','german_shepherd'),(45,'german_shepherd','german_shepherd'),(46,'golden_retriever','golden_retriever'),(47,'golden_retriever','golden_retriever'),(48,'golden_retriever','golden_retriever'),(49,'golden_retriever','golden_retriever'),(50,'golden_retriever','golden_retriever'),(51,'golden_retriever','golden_retriever'),(52,'golden_retriever','golden_retriever'),(53,'golden_retriever','golden_retriever'),(54,'golden_retriever','golden_retriever'),(55,'golden_retriever','golden_retriever'),(56,'golden_retriever','golden_retriever'),(57,'golden_retriever','golden_retriever'),(58,'golden_retriever','golden_retriever'),(59,'golden_retriever','golden_retriever'),(60,'golden_retriever','golden_retriever');
/*!40000 ALTER TABLE `test_matrix` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-22 14:49:56
